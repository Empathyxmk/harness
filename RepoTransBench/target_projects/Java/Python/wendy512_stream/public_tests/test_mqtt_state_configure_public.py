import pytest
from unittest.mock import MagicMock

class DummyMqttStateConfigure:
    _instances = {}
    def __init__(self, name):
        self.name = name
        self.configured = False
    @classmethod
    def getInstance(cls, name):
        if name not in cls._instances:
            cls._instances[name] = DummyMqttStateConfigure(name)
        return cls._instances[name]
    def configure(self, context):
        prop = context.getInstance()
        data = prop.getOriginal()
        if data is None:
            raise ValueError("mqtt config cannot empty")
        self.configured = True

def test_singleton_instance_public():
    DummyMqttStateConfigure._instances = {}
    a = DummyMqttStateConfigure.getInstance("uniqueOne")
    b = DummyMqttStateConfigure.getInstance("uniqueOne")
    assert a is b
    c = DummyMqttStateConfigure.getInstance("uniqueTwo")
    assert a is not c

def test_configure_throws_on_null_public():
    DummyMqttStateConfigure._instances = {}
    instance = DummyMqttStateConfigure.getInstance("cfgPublic")
    context = MagicMock()
    context.getInstance.return_value.getOriginal.return_value = None
    with pytest.raises(ValueError) as ex:
        instance.configured = False
        instance.configure(context)
    assert "mqtt config cannot empty" in str(ex.value).lower()

def test_configure_success_idempotent_public():
    DummyMqttStateConfigure._instances = {}
    instance = DummyMqttStateConfigure.getInstance("anotherUnique")
    context = MagicMock()
    context.getInstance.return_value.getOriginal.return_value = {"fooPublic": "barPublic"}
    instance.configured = False
    instance.configure(context)
    instance.configure(context)