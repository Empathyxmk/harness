import pytest
from unittest.mock import Mock

class Constants:
    OP_MESSAGE_REPLY = 200

class Proto:
    def setOperation(self, op): pass
    def setBody(self, body): pass

class MsgService:
    def receive(self, proto): pass

class MessageOperation:
    def __init__(self):
        self.msgService = None

    def checkAuth(self, proto):
        pass

    def action(self, channel, proto):
        self.checkAuth(proto)
        self.msgService.receive(proto)
        proto.setOperation(Constants.OP_MESSAGE_REPLY)
        proto.setBody(None)
        channel.writeAndFlush(proto)

def test_action_calls_expected_methods():
    op = MessageOperation()
    op.msgService = Mock(spec=MsgService)
    channel = Mock()
    proto = Mock(spec=Proto)
    op.checkAuth = Mock()
    channel.writeAndFlush = Mock()
    op.action(channel, proto)
    op.msgService.receive.assert_called_once_with(proto)
    proto.setOperation.assert_called_once_with(Constants.OP_MESSAGE_REPLY)
    proto.setBody.assert_called_once_with(None)
    channel.writeAndFlush.assert_called_once_with(proto)