import pytest

from scrapy_jsonrpc.txweb import JsonResource

class DummyRequest:
    def __init__(self):
        self.headers = {}
        self._headers = {}
    def setHeader(self, k, v):
        self._headers[k] = v

def test_jsonresource_render_object_sets_headers_and_returns_json():
    jr = JsonResource()
    obj = {"foo": "bar"}
    dr = DummyRequest()
    res = jr.render_object(obj, dr)
    assert isinstance(res, str)
    assert res.strip().startswith("{") and res.strip().endswith("}")
    # check headers set
    assert dr._headers['Content-Type'] == 'application/json'
    assert dr._headers['Access-Control-Allow-Origin'] == '*'
    assert dr._headers['Access-Control-Allow-Methods'] == 'GET, POST, PATCH, PUT, DELETE'
    assert dr._headers['Access-Control-Allow-Headers'] == ' X-Requested-With'
    assert dr._headers['Content-Length'] == len(res)