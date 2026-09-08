import pytest
from unittest.mock import MagicMock, patch
import threading

class DummyPulsarStateConfigure:
    _instances = {}
    _lock = threading.Lock()
    def __init__(self, name):
        self.name = name
        self.configured = False
        self._client = None
    @classmethod
    def getInstance(cls, name):
        with cls._lock:
            if name not in cls._instances:
                cls._instances[name] = DummyPulsarStateConfigure(name)
            return cls._instances[name]
    def configure(self, config_ctx):
        if not self.configured:
            data = config_ctx.getInstance().getOriginal()
            if data is None:
                raise ValueError("pulsar sink config cannot empty")
            self.configured = True
            self._client = "clientobj"
    def getClient(self):
        return self._client

def test_singleton_instance():
    DummyPulsarStateConfigure._instances = {}
    a = DummyPulsarStateConfigure.getInstance("foo")
    b = DummyPulsarStateConfigure.getInstance("foo")
    assert a is b
    c = DummyPulsarStateConfigure.getInstance("bar")
    assert a is not c

def test_configure_throws_on_null_config():
    DummyPulsarStateConfigure._instances = {}
    instance = DummyPulsarStateConfigure.getInstance("cfgtest")
    instance.configured = False
    context = MagicMock()
    context.getInstance.return_value.getOriginal.return_value = None
    with pytest.raises(ValueError) as ex:
        instance.configured = False
        instance.configure(context)
    assert "pulsar sink config cannot empty" in str(ex.value)

def test_configure_success_and_idempotent():
    DummyPulsarStateConfigure._instances = {}
    instance = DummyPulsarStateConfigure.getInstance("idemp")
    context = MagicMock()
    context.getInstance.return_value.getOriginal.return_value = {"foo": "bar"}
    with patch.object(DummyPulsarStateConfigure, 'getClient', return_value='clientobj'):
        instance.configured = False
        instance.configure(context)
        assert instance.getClient() == "clientobj"
        # idempotent
        instance.configure(context)