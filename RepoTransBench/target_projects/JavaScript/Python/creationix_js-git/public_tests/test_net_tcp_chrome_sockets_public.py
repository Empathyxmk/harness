import pytest
from unittest import mock
import time

class DummyChromeSocketsTcp:
    def __init__(self):
        self.onReceive = type('', (), {"addListener": lambda self, x: None})()
        self.onReceiveError = type('', (), {"addListener": lambda self, x: None})()
        self.create = mock.Mock()
        self.connect = mock.Mock()
        self.getInfo = mock.Mock()
        self.setPaused = mock.Mock()
        self.close = mock.Mock()
        self.send = mock.Mock()

class DummyWindow:
    def __init__(self):
        self.chrome = type('', (), {})()
        self.chrome.sockets = type('', (), {})()
        self.chrome.sockets.tcp = DummyChromeSocketsTcp()
        self.chrome.runtime = type('', (), {"lastError": type('', (), {"message": "test-error-public"})()})()

@pytest.fixture(autouse=True)
def patch_globals(monkeypatch):
    dummy_win = DummyWindow()
    monkeypatch.setattr("builtins.window", dummy_win)
    return dummy_win

class DummyChannel:
    def __init__(self):
        self.put = lambda val=None: None
        self.drain = lambda cb=None: None
        self.take = lambda cb=None: None

def connect(host=None, port=None, onError=None):
    if not host or not port:
        raise Exception("host and port")
    return DummyChannel()

def test_throws_on_missing_host_port_public():
    with pytest.raises(Exception, match="host and port"):
        connect(None, None, lambda: None)
    with pytest.raises(Exception, match="host and port"):
        connect("", 0, lambda: None)

def test_calls_create_and_listeners_public(patch_globals):
    patch_globals.chrome.sockets.tcp.create.side_effect = lambda cb: cb({"socketId": 200})
    patch_globals.chrome.sockets.tcp.connect.side_effect = lambda sid, host, port, cb: cb(2)
    patch_globals.chrome.sockets.tcp.getInfo.side_effect = lambda sid, cb: cb({"connected": True})
    onError = mock.Mock()
    connect("pubhost", 2345, onError)
    assert patch_globals.chrome.sockets.tcp.create.called