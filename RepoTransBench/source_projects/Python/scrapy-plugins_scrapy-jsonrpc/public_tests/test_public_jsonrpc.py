import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scrapy_jsonrpc.jsonrpc import jsonrpc_success_obj, jsonrpc_error_obj

def test_jsonrpc_success_obj_public():
    result = jsonrpc_success_obj("abcde", {"value": 99})
    assert result["jsonrpc"] == "2.0"
    assert result["id"] == "abcde"
    assert result["result"] == {"value": 99}

def test_jsonrpc_error_obj_public():
    error = jsonrpc_error_obj("xyz01", -123, "Unexpected Error")
    assert error["jsonrpc"] == "2.0"
    assert error["id"] == "xyz01"
    err = error["error"]
    assert err["code"] == -123
    assert err["message"] == "Unexpected Error"

def test_jsonrpc_error_obj_with_data_public():
    error = jsonrpc_error_obj("ab10", -20, "Message", data={"details": "extra"})
    assert error["jsonrpc"] == "2.0"
    assert error["id"] == "ab10"
    err = error["error"]
    assert err["code"] == -20
    assert err["message"] == "Message"
    assert err["data"] == {"details": "extra"}