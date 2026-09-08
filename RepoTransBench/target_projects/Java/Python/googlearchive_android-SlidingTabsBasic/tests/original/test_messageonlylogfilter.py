import pytest
from unittest.mock import Mock, ANY

class LogNode:
    def println(self, priority, tag, msg, tr):
        pass

class Log:
    NONE = 0
    WARN = 5
    ERROR = 6

class MessageOnlyLogFilter:
    def __init__(self, next_node=None):
        self._next = next_node

    def println(self, priority, tag, msg, tr):
        if self._next:
            self._next.println(Log.NONE if hasattr(Log, 'NONE') else 0, None, msg, None)

    def setNext(self, node):
        self._next = node

    def getNext(self):
        return self._next

def test_message_only_forwarded():
    next_node = Mock(spec=LogNode)
    filter_ = MessageOnlyLogFilter(next_node)

    filter_.println(Log.WARN, "Tag", "Message", RuntimeError("err"))
    next_node.println.assert_called_once_with(Log.NONE, None, "Message", None)

def test_no_next_does_nothing():
    filter_ = MessageOnlyLogFilter()
    # Should not throw or call anything
    filter_.println(Log.ERROR, "tag", "sample", None)
    # No assertion necessary

def test_set_get_next():
    filter_ = MessageOnlyLogFilter()
    assert filter_.getNext() is None
    dummy = Mock(spec=LogNode)
    filter_.setNext(dummy)
    assert filter_.getNext() is dummy