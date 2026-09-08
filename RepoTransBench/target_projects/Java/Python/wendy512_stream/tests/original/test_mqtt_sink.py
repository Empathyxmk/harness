import pytest
from unittest.mock import MagicMock, patch, call

class DummyMqttSink:
    def __init__(self):
        self.stateConfigure = None
    def configure(self, context):
        self.stateConfigure = context.getState()
        self.stateConfigure.configure(context)
    def process(self, msgs):
        # Expect each msg to have getHeaders().getString() and getPayload()
        for m in msgs:
            topic = m.getHeaders().getString("topic")
            if not topic:
                continue
            payload = m.getPayload()
            client = self.stateConfigure.getClient()
            qos = self.stateConfigure.getQos()
            client.publish(topic, type("DummyMsg", (), {"getPayload": lambda s: payload, "getQos": lambda s: qos, "payload": payload, "qos": qos})())
    def send(self, topic, payload):
        client = self.stateConfigure.getClient()
        try:
            client.publish(topic, type("DummyMsg", (), {"getPayload": lambda s: payload, "getQos": lambda s: self.stateConfigure.getQos(), "payload": payload, "qos": self.stateConfigure.getQos()})())
        except Exception:
            pass

def test_configure_calls_configure_on_state():
    context = MagicMock()
    state = MagicMock()
    context.getState.return_value = state
    sink = DummyMqttSink()
    sink.configure(context)
    state.configure.assert_called_once_with(context)

def test_process_ignores_blank_topic_and_publishes_valid():
    msg1 = MagicMock()
    msg2 = MagicMock()
    msg1.getHeaders().getString.return_value = ""
    msg2.getHeaders().getString.return_value = "topic"
    msg1.getPayload.return_value = "payload1"
    msg2.getPayload.return_value = "payload2"

    state = MagicMock()
    client = MagicMock()
    state.getClient.return_value = client
    state.getQos.return_value = 1

    context = MagicMock()
    context.getState.return_value = state

    sink = DummyMqttSink()
    sink.stateConfigure = state
    sink.process([msg1, msg2])
    client.publish.assert_called_once()
    call_args = client.publish.call_args
    assert call_args[0][0] == "topic"
    sent_msg = call_args[0][1]
    assert sent_msg.payload == "payload2"
    assert sent_msg.qos == 1

def test_send_handles_exception():
    state = MagicMock()
    client = MagicMock()
    client.publish.side_effect = Exception("error")
    state.getClient.return_value = client
    state.getQos.return_value = 0
    sink = DummyMqttSink()
    sink.stateConfigure = state
    try:
        sink.send("topic", "payload")
    except Exception:
        pytest.fail("Should not raise exception")