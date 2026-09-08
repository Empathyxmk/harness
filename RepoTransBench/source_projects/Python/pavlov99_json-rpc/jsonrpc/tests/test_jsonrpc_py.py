import pytest
from jsonrpc import jsonrpc
import json

class Dummy10Request:
    @staticmethod
    def from_data(data):
        return ("10", data)

class Dummy20Request:
    @staticmethod
    def from_data(data):
        return ("20", data)

def test_from_data_jsonrpc_key(monkeypatch):
    monkeypatch.setattr(jsonrpc, "JSONRPC10Request", Dummy10Request)
    monkeypatch.setattr(jsonrpc, "JSONRPC20Request", Dummy20Request)
    # data has "jsonrpc" -> JSONRPC20Request
    result = jsonrpc.JSONRPCRequest.from_data({"jsonrpc": "2.0", "foo": "bar"})
    assert result == ("20", {"jsonrpc": "2.0", "foo": "bar"})

def test_from_data_no_jsonrpc_key(monkeypatch):
    monkeypatch.setattr(jsonrpc, "JSONRPC10Request", Dummy10Request)
    monkeypatch.setattr(jsonrpc, "JSONRPC20Request", Dummy20Request)
    # data is dict, no "jsonrpc" -> JSONRPC10Request
    result = jsonrpc.JSONRPCRequest.from_data({"foo": "bar"})
    assert result == ("10", {"foo": "bar"})

def test_from_json_dispatch(monkeypatch):
    monkeypatch.setattr(jsonrpc, "JSONRPCRequest", jsonrpc.JSONRPCRequest)
    data = {"jsonrpc": "2.0", "foo": "baz"}
    called = {}
    class DummyClass(jsonrpc.JSONRPCRequest):
        @classmethod
        def deserialize(cls, json_str):
            called["des"] = True
            return data
        @classmethod
        def from_data(cls, dt):
            called["from_data"] = dt
            return "called"
    monkeypatch.setattr(jsonrpc, "JSONRPCRequest", DummyClass)
    assert DummyClass.from_json("{}") == "called"
    monkeypatch.setattr(jsonrpc, "JSONRPCRequest", jsonrpc.JSONRPCRequest)  # reset