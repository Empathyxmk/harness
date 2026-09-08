import pytest
from unittest.mock import Mock

class RocketMQTemplate:
    def receive(self, klass):
        return ["foo", "bar", "baz"]

class StringConsumer:
    def __init__(self):
        self.rocketMQTemplate = None

    def consume(self):
        return self.rocketMQTemplate.receive(str)

def test_consume_public():
    rocketMQTemplate = Mock()
    stringConsumer = StringConsumer()
    stringConsumer.rocketMQTemplate = rocketMQTemplate
    fakeMessages = ["foo", "bar", "baz"]
    rocketMQTemplate.receive.return_value = fakeMessages
    messages = stringConsumer.consume()
    assert len(messages) == 3
    assert "foo" in messages
    assert messages[1] == "bar"
    rocketMQTemplate.receive.assert_called_once_with(str)