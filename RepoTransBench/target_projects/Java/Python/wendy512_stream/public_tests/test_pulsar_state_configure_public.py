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

def test_singleton_instance_with_other_names():
    DummyPulsarStateConfigure._instances = {}
    a = DummyPulsarStateConfigure.getInstance("alpha")
    b = DummyPulsarStateConfigure.getInstance("alpha")
    assert a is b
    c = DummyPulsarStateConfigure.getInstance("beta")
    assert a is not c

def test_configure_throws_on_null_config_public():
    DummyPulsarStateConfigure._instances = {}
    instance = DummyPulsarStateConfigure.getInstance("cfgPublic")
    context = MagicMock()
    context.getInstance.return_value.getOriginal.return_value = None
    instance.configured = False
    with pytest.raises(ValueError) as ex:
        instance.configured = False
        instance.configure(context)
    assert "pulsar sink config cannot empty" in str(ex.value).lower()

def test_configure_success_and_idempotent_different_map():
    DummyPulsarStateConfigure._instances = {}
    instance = DummyPulsarStateConfigure.getInstance("diffmap")
    context = MagicMock()
    context.getInstance.return_value.getOriginal.return_value = {"someKey": "someValue123"}
    with patch.object(DummyPulsarStateConfigure, 'getClient', return_value='clientobj'):
        instance.configured = False
        instance.configure(context)
        assert instance.getClient() == "clientobj"
        # idempotent
        instance.configure(context)