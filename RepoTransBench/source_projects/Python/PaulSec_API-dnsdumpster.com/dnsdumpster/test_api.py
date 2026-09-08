import pytest
from dnsdumpster import DNSDumpsterAPI

def test_dnsdumpsterapi_class_available():
    assert hasattr(DNSDumpsterAPI, "search")
    assert callable(getattr(DNSDumpsterAPI, "search"))

def test_dnsdumpsterapi_search_type(monkeypatch):
    api = DNSDumpsterAPI()
    monkeypatch.setattr(api.session, "get", lambda url: type('resp', (object,), {"text": "<html><form><input name='csrfmiddlewaretoken' value='fake'></form></html>", "status_code": 200, "headers": {}})())
    monkeypatch.setattr(api.session, "post", lambda url, data, headers: type('resp', (object,), {"text": "<html><table></table></html>", "status_code": 200, "headers": {}})())
    res = api.search("test.com")
    assert isinstance(res, dict)

def test_dnsdumpsterapi_search_invalid(monkeypatch):
    # test input that causes csrf not found
    api = DNSDumpsterAPI()
    monkeypatch.setattr(api.session, "get", lambda url: type('resp', (object,), {"text": "<html></html>", "status_code": 200, "headers": {}})())
    with pytest.raises(Exception):
        api.search("fail.com")