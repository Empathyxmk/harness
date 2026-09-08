import pytest
import types
import requests
from jsonapi_requests import request_factory, configuration, data as ja_data

class DummyConfig:
    API_ROOT = "http://test"
    APPEND_SLASH = True
    RETRIES = 1
    VALIDATE_SSL = True
    AUTH = None
    TIMEOUT = None

class DummyObject:
    def as_data(self):
        return {"type": "abc", "id": "xyz"}

def make_response(status_code=200, content=None, json_data=None):
    response = requests.models.Response()
    response.status_code = status_code
    if content is not None:
        response._content = content
    else:
        response._content = b'{}'
    if json_data is not None:
        def fake_json():
            return json_data
        response.json = fake_json
    else:
        def fake_json_fail():
            raise ValueError()
        response.json = fake_json_fail
    return response

def test_object_json_assertion(monkeypatch):
    config = DummyConfig()
    f = request_factory.ApiRequestFactory(config)

    # Monkeypatch the retrying property getter on the class to return our custom function
    monkeypatch.setattr(request_factory.ApiRequestFactory, "retrying", property(lambda self: lambda func, *a, **kwa: func(*a, **kwa)), raising=False)
    obj = DummyObject()
    # Mock requests.request so no HTTP request is actually made
    def dummy_request(method, url, headers=None, **kwargs):
        class DummyResp:
            status_code = 200
            def json(self): return {"ok": 1}
            content = b'{"ok": 1}'
        return DummyResp()
    monkeypatch.setattr(request_factory.requests, "request", dummy_request)

    ret = f.request("api", "POST", object=obj)
    assert ret is not None
    with pytest.raises(AssertionError):
        f.request("api", "POST", object=obj, json={"bad": "yes"})

def test_build_absolute_url_slash():
    config = DummyConfig()
    config.API_ROOT = "http://test/api/"
    config.APPEND_SLASH = True
    fact = request_factory.ApiRequestFactory(config)
    url = fact._build_absolute_url("foo")
    assert url.endswith("/")
    config.APPEND_SLASH = False
    url2 = fact._build_absolute_url("foo")
    assert url2.rstrip('/').endswith('foo')

def test_parse_response_paths():
    config = DummyConfig()
    fact = request_factory.ApiRequestFactory(config)
    resp = make_response(500, content=b'ERR')
    with pytest.raises(request_factory.ApiInternalServerError):
        fact._parse_response(resp)
    resp = make_response(204)
    result = fact._parse_response(resp)
    assert isinstance(result, request_factory.ApiResponse)
    resp = make_response(400, content=b'ERR')
    with pytest.raises(request_factory.ApiClientError):
        fact._parse_response(resp)
    resp = make_response(200, content=b'oops')
    with pytest.raises(request_factory.ApiInvalidResponseError):
        fact._parse_response(resp)
    resp = make_response(200, json_data={"hello": "world"})
    result = fact._parse_response(resp)
    assert result.payload == {"hello": "world"}

def test_request_connection(monkeypatch):
    config = DummyConfig()
    fact = request_factory.ApiRequestFactory(config)

    class DummyReq:
        attempts = 0

        @staticmethod
        def request(*args, **kwargs):
            DummyReq.attempts += 1
            if DummyReq.attempts < 2:
                raise requests.ConnectionError()
            class DummyResp:
                status_code = 200
                def json(self): return {"a": "b"}
                content = b""
            return DummyResp()

    monkeypatch.setattr(request_factory.requests, "request", DummyReq.request)
    # Patch the retrying property getter on the class
    monkeypatch.setattr(request_factory.ApiRequestFactory, "retrying", property(lambda self: lambda func, *a, **kwa: func(*a, **kwa)), raising=False)
    # Should raise ApiConnectionError after connection error
    with pytest.raises(request_factory.ApiConnectionError):
        fact._request("http://t", "GET")

def test_configured_options_variants():
    conf = DummyConfig()
    fact = request_factory.ApiRequestFactory(conf)
    opts = fact.configured_options
    assert opts["verify"] is True
    conf.AUTH = "BASIC"
    conf.TIMEOUT = 10
    opts = fact.configured_options
    assert opts["auth"] == "BASIC"
    assert opts["timeout"] == 10

def test_api_response_repr_data(monkeypatch):
    resp = request_factory.ApiResponse(123, {"foo": "bar"})

    class DummyJAR:
        @staticmethod
        def from_data(payload):
            class DummyContent:
                data = None
            return DummyContent()
    monkeypatch.setattr(request_factory.data, "JsonApiResponse", DummyJAR)
    val = resp.data
    assert val == {}

    class DummyJAR2:
        @staticmethod
        def from_data(payload):
            class DummyContent:
                data = {"x": 42}
            return DummyContent()
    monkeypatch.setattr(request_factory.data, "JsonApiResponse", DummyJAR2)
    resp2 = request_factory.ApiResponse(123, {"foo": "bar"})
    r2 = resp2.data
    assert r2 == {"x": 42}
    assert repr(resp2) == "<ApiResponse({'foo': 'bar'})>"

def test_error_inits():
    e = request_factory.ApiInvalidResponseError(404, b'abc')
    assert e.status_code == 404
    assert e.content == b'abc'
    assert issubclass(request_factory.ApiInternalServerError, request_factory.ApiInvalidResponseError)
    assert issubclass(request_factory.ApiClientError, request_factory.ApiInvalidResponseError)
    assert issubclass(request_factory.ApiConnectionError, request_factory.ApiRequestError)