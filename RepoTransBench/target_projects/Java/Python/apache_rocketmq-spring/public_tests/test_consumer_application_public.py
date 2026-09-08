import pytest
from unittest.mock import Mock

class ConsumerApplication:
    def __init__(self):
        self.rocketMQTemplate = None
        self.extRocketMQTemplate = None

    def run(self):
        self.rocketMQTemplate.receive(str)
        self.extRocketMQTemplate.receive(str)

    @staticmethod
    def main(args):
        pass

def test_run_public():
    rocketMQTemplate = Mock()
    extRocketMQTemplate = Mock()
    consumerApplication = ConsumerApplication()
    mockList = ["msgA", "msgB"]
    rocketMQTemplate.receive.return_value = mockList
    extRocketMQTemplate.receive.return_value = mockList

    consumerApplication.rocketMQTemplate = rocketMQTemplate
    consumerApplication.extRocketMQTemplate = extRocketMQTemplate

    consumerApplication.run()
    rocketMQTemplate.receive.assert_called_once_with(str)
    extRocketMQTemplate.receive.assert_called_once_with(str)

def test_main_public():
    ConsumerApplication.main(["testPublic"])