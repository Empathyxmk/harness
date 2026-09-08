import pytest
from unittest.mock import Mock, call

class RocketMQTemplate:
    def sendOneWay(self, topic, msg):
        pass
    def syncSend(self, topic, msg):
        return None

def test_send_and_receive_with_different_data():
    rocketMQTemplate = Mock(spec=RocketMQTemplate)
    msg = {"payload": "HelloPublic", "header": {"KEYS": "pubKey-789"}}
    rocketMQTemplate.sendOneWay.return_value = None
    rocketMQTemplate.sendOneWay("public-topic", msg)
    rocketMQTemplate.sendOneWay.assert_called_once_with("public-topic", msg)

def test_sync_send_returns_null():
    rocketMQTemplate = Mock(spec=RocketMQTemplate)
    rocketMQTemplate.syncSend.return_value = None
    result = rocketMQTemplate.syncSend("testSyncPUB", "public-body-123")
    assert result is None