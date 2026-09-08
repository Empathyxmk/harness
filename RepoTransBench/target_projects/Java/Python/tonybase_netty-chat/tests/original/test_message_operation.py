import pytest
from unittest.mock import Mock

# Minimal stubs for constants, proto, and dependencies
class Constants:
    OP_MESSAGE = 100
    OP_MESSAGE_REPLY = 200

class Proto:
    def setOperation(self, op): pass
    def setBody(self, body): pass

class MsgService:
    def receive(self, proto): pass

class MessageOperation:
    def __init__(self):
        self.msgService = None
        self._op = Constants.OP_MESSAGE

    def op(self):
        return self._op

    def checkAuth(self, proto):
        pass

    def action(self, channel, proto):
        self.checkAuth(proto)
        self.msgService.receive(proto)
        proto.setOperation(Constants.OP_MESSAGE_REPLY)
        proto.setBody(None)
        channel.writeAndFlush(proto)

@pytest.fixture
def message_operation_test_setup():
    op = MessageOperation()
    msg_service = Mock(spec=MsgService)
    channel = Mock()
    op.msgService = msg_service
    return op, msg_service, channel

def test_op(message_operation_test_setup):
    op, msg_service, channel = message_operation_test_setup
    assert op.op() == Constants.OP_MESSAGE

def test_action_writes_reply(message_operation_test_setup):
    op, msg_service, channel = message_operation_test_setup
    proto = Mock(spec=Proto)

    # Patch checkAuth to do nothing
    op.checkAuth = Mock()
    # Patch channel's method to match Java's writeAndFlush
    channel.writeAndFlush = Mock()

    op.action(channel, proto)

    msg_service.receive.assert_called_once_with(proto)
    proto.setOperation.assert_called_once_with(Constants.OP_MESSAGE_REPLY)
    proto.setBody.assert_called_once_with(None)
    channel.writeAndFlush.assert_called_once_with(proto)