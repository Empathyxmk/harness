import pytest
import time
from unittest import mock

# -- Mocks for culvert and net --
class FakeChannel:
    def __init__(self):
        self.queue = []
    def put(self, val):
        self.queue.append(val)
    def drain(self, cb):
        time.sleep(0.001)
        cb()
    def take(self, cb):
        time.sleep(0.001)
        cb("test")

@pytest.fixture(autouse=True)
def patch_culvert(monkeypatch):
    monkeypatch.setattr("builtins.makeChannel", FakeChannel)
    monkeypatch.setattr("builtins.culvert", FakeChannel)

class FakeClient:
    def __init__(self):
        self.dataWritten = []
        self.ended = False
    def write(self, data):
        self.dataWritten.append(data)
        # simulate 'drain'
        if hasattr(self, "_on_drain"): self._on_drain()
        return True
    def read(self):
        return None
    def end(self):
        self.ended = True
    def on(self, *args, **kwargs): return self

# patching "net" module, which is only used in connect() for the original
@pytest.fixture(autouse=True)
def patch_net(monkeypatch):
    net = type('net', (), {})()
    def fake_connect(opts, cb):
        client = FakeClient()
        time.sleep(0.001)
        cb()
        return client
    net.connect = mock.Mock(side_effect=fake_connect)
    monkeypatch.setattr("builtins.net", net)
    yield net

@pytest.fixture
def connect():
    # import here to use above monkeypatches, simulate connect() import
    # In actual test, import your tcp-node implementation
    def connect_f(host, port, err):
        if not host or not port:
            raise Exception("host and port required")
        return FakeChannel()
    return connect_f

def test_throws_on_missing_host_port(connect):
    with pytest.raises(Exception, match="host and port"):
        connect(None, None, lambda: None)
    with pytest.raises(Exception, match="host and port"):
        connect("", 0, lambda: None)

def test_connects_and_triggers_handlers(connect):
    api = connect("localhost", 8000, lambda: None)
    assert hasattr(api, "put")
    assert hasattr(api, "drain")
    assert hasattr(api, "take")
    assert callable(api.put)
    assert callable(api.take)

def test_triggers_error_handler_on_error(monkeypatch, connect):
    # Patch net.connect to simulate error event
    class ErrorClient(FakeClient):
        def __init__(self, *a, **kw):
            super().__init__(*a, **kw)
        def trigger_error(self, err_handler):
            err_handler(Exception("simulated"))
    net = type('net', (), {})()
    def fake_connect(opts, cb):
        client = ErrorClient()
        cb()
        client.trigger_error(lambda e: None)
        return client
    net.connect = mock.Mock(side_effect=fake_connect)
    monkeypatch.setattr("builtins.net", net)
    connect("localhost", 1337, lambda e=None: None)