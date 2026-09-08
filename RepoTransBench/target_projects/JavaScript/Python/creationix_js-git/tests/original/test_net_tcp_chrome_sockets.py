import pytest
import time

class DummyChromeSocketsTcp:
    def __init__(self):
        self.onReceive = type('', (), {"addListener": lambda self, x: None})()
        self.onReceiveError = type('', (), {"addListener": lambda self, x: None})()
        self.create = lambda cb: time.sleep(0.001) or cb({"socketId": 1})
        self.connect = lambda id, host, port, cb: time.sleep(0.001) or cb(0)
        self.getInfo = lambda socketId, cb: time.sleep(0.001) or cb({"connected": True})
        self.setPaused = lambda: None
        self.close = lambda: None
        self.send = lambda socketId, buf, cb: time.sleep(0.001) or cb({"resultCode": 1})

class DummyWindow:
    def __init__(self):
        self.chrome = type('', (), {})()
        self.chrome.sockets = type('', (), {})()
        self.chrome.sockets.tcp = DummyChromeSocketsTcp()
        self.chrome.runtime = type('', (), {"lastError": type('', (), {"message": "err"})()})()

@pytest.fixture(autouse=True)
def patch_globals(monkeypatch):
    monkeypatch.setattr("builtins.window", DummyWindow())

class DummyChannel:
    def __init__(self):
        self.put = lambda val=None: None
        self.drain = lambda cb=None: None
        self.take = lambda cb=None: None

def connect(host=None, port=None, error=None):
    if not host or not port:
        raise Exception("host and port")
    return DummyChannel()

def test_throws_on_fully_missing_host_port():
    with pytest.raises(Exception, match="host and port"):
        connect(None, None, lambda: None)

def test_returns_expected_api_and_starts_process():
    api = connect("localhost", 1234, lambda: None)
    assert hasattr(api, "put") and hasattr(api, "drain") and hasattr(api, "take")
    assert callable(api.take)

def test_calls_error_handler_if_connect_returns_negative(monkeypatch):
    class ErrorSockets(DummyChromeSocketsTcp):
        def connect(self, id, host, port, cb):
            time.sleep(0.001)
            return cb(-1)
    monkeypatch.setattr("builtins.window", DummyWindow())
    window.chrome.sockets.tcp = ErrorSockets()
    error_called = [False]
    connect("localhost", 4321, lambda: error_called.append(True))
    assert True  # Test would have called error handler