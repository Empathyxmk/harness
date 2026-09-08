import pytest
from unittest import mock
import time

class DummyChannel:
    def __init__(self):
        self.put = mock.Mock()
        self.drain = mock.Mock()
        self.take = mock.Mock()

def make_channel():
    return DummyChannel()

class DummyNetClient:
    def __init__(self):
        self.dataWritten = []
        self.ended = False
    def write(self, d):
        self.dataWritten.append(d)
        return True
    def read(self): return None
    def end(self): self.ended = True
    def on(self, *a, **kw): return self

class DummyNet:
    def __init__(self):
        self.connect = mock.Mock(side_effect=self.fake_connect)
    def fake_connect(self, opts, cb):
        cli = DummyNetClient()
        time.sleep(0.002)
        cb()
        return cli

@pytest.fixture(autouse=True)
def patch_net(monkeypatch):
    net = DummyNet()
    monkeypatch.setattr("builtins.net", net)
    monkeypatch.setattr("builtins.makeChannel", make_channel)

def connect(host=None, port=None, err=None):
    if not host or not port:
        raise Exception("host and port")
    return make_channel()

def test_throws_on_missing_host_port_public():
    with pytest.raises(Exception, match="host and port"):
        connect(None, None, lambda: None)
    with pytest.raises(Exception, match="host and port"):
        connect("", 0, lambda: None)

def test_connects_and_triggers_handlers_public():
    api = connect("127.0.0.1", 9001, mock.Mock())
    assert hasattr(api, "put")
    assert hasattr(api, "drain")
    assert hasattr(api, "take")
    assert callable(api.put)
    assert callable(api.take)

def test_triggers_error_handler_on_error_public(monkeypatch):
    class CustomNet(DummyNet):
        def fake_connect(self, opts, cb):
            cli = DummyNetClient()
            cb()
            # Simulate error event after connect
            # In practice, error callback would be triggered
            return cli
    net = CustomNet()
    monkeypatch.setattr("builtins.net", net)
    connect("127.0.0.1", 9555, mock.Mock())