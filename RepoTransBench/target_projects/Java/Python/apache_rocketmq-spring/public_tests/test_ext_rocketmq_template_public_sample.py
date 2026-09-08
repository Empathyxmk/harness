import pytest
from unittest.mock import Mock

class RocketMQTemplate:
    def receive(self, cls):
        return ["alpha", "beta", "gamma"]

class ExtRocketMQTemplate:
    def __init__(self):
        self.rocketMQTemplate = None

    def receiveMessage(self):
        return self.rocketMQTemplate.receive(str)

def test_receive_message_public():
    rocketMQTemplate = Mock()
    extRocketMQTemplate = ExtRocketMQTemplate()
    extRocketMQTemplate.rocketMQTemplate = rocketMQTemplate
    mockResult = ["alpha", "beta", "gamma"]
    rocketMQTemplate.receive.return_value = mockResult
    received = extRocketMQTemplate.receiveMessage()
    assert len(received) == 3
    assert received[0] == "alpha"
    assert "beta" in received
    rocketMQTemplate.receive.assert_called_once_with(str)