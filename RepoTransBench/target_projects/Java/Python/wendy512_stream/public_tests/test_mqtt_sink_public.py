import pytest
from unittest.mock import MagicMock, patch

class DummyMqttSink:
    def __init__(self):
        self.stateConfigure = None
    def configure(self, context):
        self.stateConfigure = context.getState()
        self.stateConfigure.configure(context)

def test_configure_and_init_producer_public():
    sink = DummyMqttSink()
    context = MagicMock()
    state = MagicMock()
    context.getState.return_value = state
    context.getConfig.return_value.getOriginal.return_value = {
        "topicName": "public-mqtt-topic",
        "connection": "tcp://public-mqtt-broker:1883"
    }
    sink.configure(context)
    state.configure.assert_called_once_with(context)