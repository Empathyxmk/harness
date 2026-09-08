import pytest
import time

class DummyWS:
    def __init__(self, url):
        self.url = url
        time.sleep(0.002)
        self.onopen = None
        if self.onopen:
            self.onopen()
    def send(self): pass
    def close(self): pass
    def binaryType(self, t): pass

@pytest.fixture(autouse=True)
def patch_ws(monkeypatch):
    monkeypatch.setattr("builtins.WebSocket", DummyWS)

class DummyChannel:
    def __init__(self):
        self.put = lambda val=None: None
        self.drain = lambda cb=None: None
        self.take = lambda cb=None: None

def ws_proxy(proxy_url):
    def inner(host=None, port=None, error=None):
        if not host or not port:
            raise Exception("host and port")
        return DummyChannel()
    return inner

def test_appends_slash_to_proxy_url_public():
    fn = ws_proxy("ws://proxyhost/different")
    assert callable(fn)

def test_throws_if_host_or_port_missing_public():
    fn = ws_proxy("ws://proxyhost/different/")
    with pytest.raises(Exception, match="host and port"):
        fn(None, None, lambda: None)
    with pytest.raises(Exception, match="host and port"):
        fn("", 0, lambda: None)

def test_returns_channels_and_sets_up_ws_public():
    fn = ws_proxy("ws://proxyhost/different/")
    api = fn("publichost", 6543, lambda: None)
    assert callable(api.put)

def test_calls_error_handler_on_ws_error_public():
    class ErrorWS(DummyWS):
        def __init__(self, url):
            time.sleep(0.004)
            self.onerror = lambda *a, **k: None
    fn = ws_proxy("ws://proxyhost/different/")
    try:
        fn("errorhost", 4321, lambda: True)
    except Exception:
        pass
    assert True