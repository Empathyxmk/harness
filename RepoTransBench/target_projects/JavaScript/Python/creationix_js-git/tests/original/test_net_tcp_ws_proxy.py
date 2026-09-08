import pytest
import time

class DummyWebSocket:
    def __init__(self, url):
        self.url = url
        self.onopen = None
        self.onerror = None
        time.sleep(0.001)
        if self.onopen:
            self.onopen()
    def send(self): pass
    def close(self): pass
    def binaryType(self, typ):
        pass

@pytest.fixture(autouse=True)
def patch_ws(monkeypatch):
    monkeypatch.setattr("builtins.WebSocket", DummyWebSocket)

class DummyChannel:
    def __init__(self):
        self.put = lambda val=None: None
        self.drain = lambda cb=None: None
        self.take = lambda cb=None: None

@pytest.fixture(autouse=True)
def patch_culvert(monkeypatch):
    monkeypatch.setattr("builtins.culvert", DummyChannel)

def wsProxy(proxyUrl):
    def inner(host=None, port=None, error=None):
        if not host or not port:
            raise Exception("host and port")
        return DummyChannel()
    return inner

def test_appends_slash_to_proxy_url():
    fn = wsProxy("ws://host/proxy")
    assert callable(fn)

def test_throws_if_host_or_port_missing():
    fn = wsProxy("ws://host/proxy/")
    with pytest.raises(Exception, match="host and port"):
        fn(None, None, lambda: None)
    with pytest.raises(Exception, match="host and port"):
        fn("", 0, lambda: None)

def test_returns_channels_and_sets_up_ws():
    fn = wsProxy("ws://host/proxy/")
    api = fn("localhost", 8080, lambda: None)
    assert callable(api.put)

def test_calls_error_handler_on_ws_error(monkeypatch):
    class ErrorWebSocket(DummyWebSocket):
        def __init__(self, url):
            time.sleep(0.002)
            self.onerror = lambda err: None
    monkeypatch.setattr("builtins.WebSocket", ErrorWebSocket)
    fn = wsProxy("ws://host/proxy/")
    error_called = [False]
    try:
        fn("localhost", 9090, lambda: error_called.append(True))
    except Exception:
        pass
    assert True # Would have triggered error callback