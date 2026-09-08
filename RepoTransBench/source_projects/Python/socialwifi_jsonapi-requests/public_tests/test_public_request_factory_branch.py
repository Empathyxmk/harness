import pytest
import types
import requests
from jsonapi_requests import request_factory, configuration, data as ja_data

class DummyConfigPublic:
    API_ROOT = "http://public"
    APPEND_SLASH = False
    RETRIES = 2
    VALIDATE_SSL = False
    AUTH = None
    TIMEOUT = None

class DummyObjectPublic:
    def as_data(self):
        return {"type": "resource", "id": "abc"}

def make_response_public(status_code=202, content=None, json_data=None):
    response = requests.models.Response()
    response.status_code = status_code
    if content is not None:
        response._content = content
    else:
        response._content = b'{"foo": "bar"}'
    if json_data is not None:
        def fake_json():
            return json_data
        response.json = fake_json
    else:
        def fake_json_fail():
            raise ValueError()
        response.json = fake_json_fail
    return response

def test_object_json_assertion_public(monkeypatch):
    config = DummyConfigPublic()
    f = request_factory.ApiRequestFactory(config)

    # Retrying patch
    monkeypatch.setattr(request_factory.ApiRequestFactory, "retrying", property(lambda self: lambda func, *a, **kwa: func(*a, **kwa)), raising=False)
    obj = DummyObjectPublic()
    # Mock
    def dummy_request(method, url, headers=None, **kwargs):
        class DummyResp:
            status_code = 201
            def json(self): return {"bar": 2}
            content = b'{"bar": 2}'
        return DummyResp()
    monkeypatch.setattr(request_factory.requests, "request", dummy_request)

    ret = f.request("public_api", "POST", object=obj)
    assert ret is not None
    with pytest.raises(AssertionError):
        f.request("public_api", "POST", object=obj, json={"bad": "input"})

def test_build_absolute_url_slash_public():
    config = DummyConfigPublic()
    config.API_ROOT = "http://public/api/"
    config.APPEND_SLASH = True
    fact = request_factory.ApiRequestFactory(config)
    url = fact._build_absolute_url("bar")
    assert url.endswith("/")
    config.APPEND_SLASH = False
    url2 = fact._build_absolute_url("bar")
    assert url2.rstrip('/').endswith('bar')

def test_parse_response_paths_public():
    config = DummyConfigPublic()
    fact = request_factory.ApiRequestFactory(config)
    resp = make_response_public(501, content=b'ERROR')
    with pytest.raises(request_factory.ApiInternalServerError):
        fact._parse_response(resp)
    resp = make_response_public(204)
    result = fact._parse_response(resp)
    assert isinstance(result, request_factory.ApiResponse)
    resp = make_response_public(404, content=b'ERROR')
    with pytest.raises(request_factory.ApiClientError):
        fact._parse_response(resp)
    resp = make_response_public(200, content=b'invalid-json')
    with pytest.raises(request_factory.ApiInvalidResponseError):
        fact._parse_response(resp)
    resp = make_response_public(200, json_data={"foo": "baz"})
    result = fact._parse_response(resp)
    assert result.payload == {"foo": "baz"}

def test_request_connection_public(monkeypatch):
    config = DummyConfigPublic()
    fact = request_factory.ApiRequestFactory(config)

    class DummyReq:
        attempts = 0

        @staticmethod
        def request(*args, **kwargs):
            DummyReq.attempts += 1
            if DummyReq.attempts < 3:
                raise requests.ConnectionError()
            class DummyResp:
                status_code = 202
                def json(self): return {"z": "y"}
                content = b""
            return DummyResp()

    monkeypatch.setattr(request_factory.requests, "request", DummyReq.request)
    # Patch the retrying property getter on the class
    monkeypatch.setattr(request_factory.ApiRequestFactory, "retrying", property(lambda self: lambda func, *a, **kwa: func(*a, **kwa)), raising=False)
    # Should raise ApiConnectionError after connection errors
    with pytest.raises(request_factory.ApiConnectionError):
        fact._request("http://z", "GET")

def test_configured_options_variants_public():
    conf = DummyConfigPublic()
    fact = request_factory.ApiRequestFactory(conf)
    opts = fact.configured_options
    assert opts["verify"] is False
    conf.AUTH = "TOKEN"
    conf.TIMEOUT = 30
    opts = fact.configured_options
    assert opts["auth"] == "TOKEN"
    assert opts["timeout"] == 30

def test_api_response_repr_data_public(monkeypatch):
    resp = request_factory.ApiResponse(777, {"foo": "baz"})

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
                data = {"y": 100}
            return DummyContent()
    monkeypatch.setattr(request_factory.data, "JsonApiResponse", DummyJAR2)
    resp2 = request_factory.ApiResponse(888, {"hello": "world"})
    r2 = resp2.data
    assert r2 == {"y": 100}
    assert repr(resp2) == "<ApiResponse({'hello': 'world'})>"

def test_error_inits_public():
    e = request_factory.ApiInvalidResponseError(418, b'tea')
    assert e.status_code == 418
    assert e.content == b'tea'
    assert issubclass(request_factory.ApiInternalServerError, request_factory.ApiInvalidResponseError)
    assert issubclass(request_factory.ApiClientError, request_factory.ApiInvalidResponseError)
    assert issubclass(request_factory.ApiConnectionError, request_factory.ApiRequestError)