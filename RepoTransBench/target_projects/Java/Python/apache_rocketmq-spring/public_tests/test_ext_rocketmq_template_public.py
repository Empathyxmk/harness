import pytest
from unittest.mock import Mock, ANY

class RocketMQTemplate:
    def syncSend(self, topic, msg):
        pass

class ExtRocketMQTemplate:
    def __init__(self):
        self.rocketMQTemplate = None

    def setRocketMQTemplate(self, rocketMQTemplate):
        self.rocketMQTemplate = rocketMQTemplate

    def sendStringMessage(self, topic, payload):
        return self.rocketMQTemplate.syncSend(topic, payload)

    def sendSpringMessage(self, topic, message):
        return self.rocketMQTemplate.syncSend(topic, message)

def test_send_string_message_public():
    rocketMQTemplate = Mock()
    extRocketMQTemplate = ExtRocketMQTemplate()
    extRocketMQTemplate.setRocketMQTemplate(rocketMQTemplate)
    rocketMQTemplate.syncSend.return_value = None
    extRocketMQTemplate.sendStringMessage("pubExtTopic", "msgPublic")
    rocketMQTemplate.syncSend.assert_called_once_with("pubExtTopic", "msgPublic")

def test_send_spring_message_public():
    rocketMQTemplate = Mock()
    extRocketMQTemplate = ExtRocketMQTemplate()
    extRocketMQTemplate.setRocketMQTemplate(rocketMQTemplate)
    rocketMQTemplate.syncSend.return_value = None
    springMsg = {"payload": "data42"}
    extRocketMQTemplate.sendSpringMessage("pubExtTopic", springMsg)
    rocketMQTemplate.syncSend.assert_called_with("pubExtTopic", springMsg)