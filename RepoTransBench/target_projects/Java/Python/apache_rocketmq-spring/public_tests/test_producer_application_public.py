import pytest
from unittest.mock import Mock

class ProducerApplication:
    def __init__(self):
        self.rocketMQTemplate = None
        self.topic = None

    def run(self):
        self.rocketMQTemplate.syncSend(self.topic, "Hello, World!")

    @staticmethod
    def main(args):
        pass

def test_run_public():
    rocketMQTemplate = Mock()
    producerApplication = ProducerApplication()
    producerApplication.rocketMQTemplate = rocketMQTemplate
    producerApplication.topic = "publicTopic"
    rocketMQTemplate.syncSend.return_value = Mock()
    producerApplication.run()
    rocketMQTemplate.syncSend.assert_called_once_with("publicTopic", "Hello, World!")

def test_main_public():
    ProducerApplication.main(["public"])