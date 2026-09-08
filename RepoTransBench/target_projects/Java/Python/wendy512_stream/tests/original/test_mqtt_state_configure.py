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
        host = prop.getString("host")
        if not host:
            raise ValueError("MQTT host cannot be empty")
        self.configured = True

def test_singleton_instance():
    DummyMqttStateConfigure._instances = {}
    a = DummyMqttStateConfigure.getInstance("foo")
    b = DummyMqttStateConfigure.getInstance("foo")
    assert a is b
    c = DummyMqttStateConfigure.getInstance("bar")
    assert a is not c

def test_configure_throws_on_blank_host():
    DummyMqttStateConfigure._instances = {}
    instance = DummyMqttStateConfigure.getInstance("t1")
    instance.configured = False
    context = MagicMock()
    prop = MagicMock()
    prop.getString.return_value = ""
    context.getInstance.return_value = prop
    context.getConfig.return_value.getString.return_value = "bar"
    with pytest.raises(ValueError) as ex:
        instance.configure(context)
    assert "MQTT host cannot be empty" in str(ex.value)