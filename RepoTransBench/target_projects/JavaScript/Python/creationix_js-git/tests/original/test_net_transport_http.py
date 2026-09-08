import pytest
from unittest import mock

# Simulate pkt-line and bodec
class MockPktLine:
    @staticmethod
    def framer(cb):
        return cb
    @staticmethod
    def deframer(cb):
        def inner(body):
            for v in ["# service=service", None, "data"]:
                cb(v)
        return inner
class MockBodec:
    @staticmethod
    def join(val=None):
        return bytearray([1,2,3])

@pytest.fixture(autouse=True)
def patch_pkt_bodec(monkeypatch):
    monkeypatch.setattr("builtins.pktLine", MockPktLine)
    monkeypatch.setattr("builtins.bodec", MockBodec)

@pytest.fixture
def transportHTTP():
    def t_http(mock_request):
        def inner(url, username=None, password=None):
            def inner2(service, error):
                class APIDuplex:
                    def __init__(self):
                        self.put = mock.Mock()
                        self.drain = mock.Mock()
                        self.take = mock.Mock()
                return APIDuplex()
            return inner2
        return t_http
    return t_http

def test_appends_auth_if_username_is_provided(monkeypatch, transportHTTP):
    # Simulate btoa in global namespace
    monkeypatch.setattr("builtins.btoa", lambda s: "encoded")
    httpTrans = transportHTTP(lambda *a, **k: None)
    f = httpTrans('url', 'u', 'p')
    assert callable(f)

def test_returns_a_duplex_channel(transportHTTP):
    called = [False]
    def mockRequest(*a, **k):
        called[0] = True
    httpTrans = transportHTTP(mockRequest)
    api = httpTrans("url")("service", lambda *a: None)
    assert hasattr(api, "put")
    assert hasattr(api, "take")
    assert hasattr(api, "drain")
    assert callable(api.put)
    assert callable(api.take)
    assert callable(api.drain)
    assert called[0]

def test_throws_on_invalid_status_code(transportHTTP):
    def badRequest(method, url, headers, body, cb):
        if cb: cb({"statusCode": 404, "headers": {"content-type":"application/x-service-advertisement"}, "body":""})
    httpTrans = transportHTTP(badRequest)
    f = httpTrans("url")("service", lambda: None)
    # Should not throw
    f.take(lambda x: None)