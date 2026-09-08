import pytest
import json

from scrapy_jsonrpc.jsonrpc import (
    JsonRpcError, jsonrpc_errors,
    jsonrpc_server_call, jsonrpc_error, jsonrpc_result
)

class DummyTarget(object):
    def echo(self, x): return x
    def add(self, a, b): return a+b
    def fail(self): raise ValueError("fail!")

def make_req(method, params=None, id=1):
    d = {'jsonrpc': '2.0', 'method': method, 'id': id}
    if params is not None:
        d['params'] = params
    return json.dumps(d)

def test_jsonrpc_result_error_helpers():
    assert jsonrpc_result(17, [1,2]) == {
        'jsonrpc': '2.0', 'result': [1,2], 'id': 17
    }
    e = jsonrpc_error(5, 1, "err", "trace")
    assert e['error']['code'] == 1
    assert e['error']['data'] == "trace"
    assert e['id'] == 5

def test_jsonrpc_server_call_success_list_params():
    req = make_req("add", [3,4])
    result = jsonrpc_server_call(DummyTarget(), req)
    assert result['result'] == 7

def test_jsonrpc_server_call_success_dict_params():
    req = make_req("add", {"a": 10, "b": 7})
    result = jsonrpc_server_call(DummyTarget(), req)
    assert result['result'] == 17

def test_jsonrpc_server_call_success_echo():
    req = make_req("echo", ["hi"])
    result = jsonrpc_server_call(DummyTarget(), req)
    assert result['result'] == "hi"

def test_jsonrpc_server_call_internal_error():
    req = make_req("fail")
    result = jsonrpc_server_call(DummyTarget(), req)
    assert result['error']['code'] == jsonrpc_errors.INTERNAL_ERROR
    assert "fail!" in result['error']['message'] or "fail!" in str(result['error'])

def test_jsonrpc_server_call_parse_error():
    class BadDecoder:
        def decode(self, arg): raise Exception("parsefail")
    res = jsonrpc_server_call(DummyTarget(), "badjson", json_decoder=BadDecoder())
    assert res['error']['code'] == jsonrpc_errors.PARSE_ERROR

def test_jsonrpc_server_call_invalid_request():
    # missing id or method
    for bad in [
        json.dumps({"jsonrpc":"2.0"}),
        json.dumps({"jsonrpc":"2.0","id":1}),
        json.dumps({"jsonrpc":"2.0","method":"echo"})
    ]:
        res = jsonrpc_server_call(DummyTarget(), bad)
        assert res['error']['code'] == jsonrpc_errors.INVALID_REQUEST

def test_jsonrpc_server_call_method_not_found():
    req = make_req("notfound")
    res = jsonrpc_server_call(DummyTarget(), req)
    assert res['error']['code'] == jsonrpc_errors.METHOD_NOT_FOUND

def test_jsonrpc_client_call_args_kwargs(monkeypatch):
    import scrapy_jsonrpc.jsonrpc as jrpc
    # Patch urlopen to always return fixed JSON
    class DummyResp:
        def read(self): return b'{"result":42}'
    class DummyReq:
        @staticmethod
        def urlopen(url, data):
            return DummyResp()
    monkeypatch.setattr(jrpc.urllib, 'request', DummyReq)
    res = jrpc.jsonrpc_client_call("url", "foo", 1, 2)
    assert res == 42
    # error result
    class DummyResp2:
        def read(self): return b'{"error":{"code":1,"message":"Errr","data":"D"}}'
    class DummyReq2:
        @staticmethod
        def urlopen(url, data):
            return DummyResp2()
    monkeypatch.setattr(jrpc.urllib, 'request', DummyReq2)
    with pytest.raises(jrpc.JsonRpcError) as e:
        jrpc.jsonrpc_client_call("url", "foo", 1, 2)
    # test both args and kwargs raises ValueError
    with pytest.raises(ValueError):
        jrpc.jsonrpc_client_call("url", "foo", 1, a=4)
    # test invalid jsonrpc response
    class DummyResp3:
        def read(self): return b'{"abc": 123}'
    class DummyReq3:
        @staticmethod
        def urlopen(url, data):
            return DummyResp3()
    monkeypatch.setattr(jrpc.urllib, 'request', DummyReq3)
    with pytest.raises(ValueError):
        jrpc.jsonrpc_client_call("url", "foo", 1, 2)