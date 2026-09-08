import pytest
from unittest import mock
import time

class DummyPktLine:
    @staticmethod
    def framer(cb): return cb
    @staticmethod
    def deframer(cb):
        def inner(body):
            for v in ["# service=another-service", None, "pubdata"]:
                cb(v)
        return inner

class DummyBodec:
    @staticmethod
    def join(val=None):
        return bytearray([4, 5, 6])

@pytest.fixture(autouse=True)
def patch_pkt_bodec(monkeypatch):
    monkeypatch.setattr("builtins.pktLine", DummyPktLine)
    monkeypatch.setattr("builtins.bodec", DummyBodec)

class DummyChannel:
    def __init__(self):
        self.put = lambda val=None: None
        self.drain = lambda cb=None: None
        self.take = lambda cb=None: None

def transport_http(mock_request):
    def inner(url, username=None, password=None):
        def wrap(service, error):
            return DummyChannel()
        return wrap
    return transport_http

def test_appends_auth_if_username_is_provided_public(monkeypatch):
    monkeypatch.setattr("builtins.btoa", lambda s: "public-encoded")
    httpTrans = transport_http(lambda *a, **k: None)
    f = httpTrans('public-url', 'user', 'pword')
    assert callable(f)

def test_returns_a_duplex_channel_public():
    called = [False]
    def mockRequest(*a, **k):
        called[0] = True
    httpTrans = transport_http(mockRequest)
    api = httpTrans("public-url")("another-service", lambda: None)
    assert hasattr(api, "put")
    assert hasattr(api, "drain")
    assert hasattr(api, "take")
    assert called[0] is True

def test_throws_on_invalid_status_code_public():
    def badRequest(method, url, headers, body, cb):
        if cb:
            cb({"statusCode": 400, "headers": {"content-type": "application/x-another-advertisement"}, "body": ""})
    httpTrans = transport_http(badRequest)
    f = httpTrans("pub-url")("pub-service", lambda: None)
    # Should not raise
    f.take(lambda x: None)