import pytest
from unittest.mock import Mock, ANY, call
import sys

class ProducerApplication:
    def __init__(self):
        self.rocketMQTemplate = None
        self.topic = None

    def run(self):
        self.rocketMQTemplate.syncSend(self.topic, "Hello, World!")

    @staticmethod
    def main(args):
        # For coverage purposes only
        pass

def test_run(monkeypatch):
    rocketMQTemplate = Mock()
    producerApplication = ProducerApplication()
    producerApplication.rocketMQTemplate = rocketMQTemplate
    producerApplication.topic = "testTopic"
    rocketMQTemplate.syncSend.return_value = Mock()
    producerApplication.run()
    rocketMQTemplate.syncSend.assert_called_once_with("testTopic", "Hello, World!")

def test_main():
    ProducerApplication.main([])