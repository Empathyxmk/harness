import pytest
from unittest.mock import Mock, ANY

class LogNode:
    def println(self, priority, tag, msg, tr):
        pass

class MessageOnlyLogFilter:
    def __init__(self, next_node=None):
        self._next = next_node

    def println(self, priority, tag, msg, tr):
        if self._next:
            self._next.println(priority, None, msg, None)

    def setNext(self, node):
        self._next = node

    def getNext(self):
        return self._next

def test_filters_message_only_different_input():
    filter_ = MessageOnlyLogFilter()
    child = Mock(spec=LogNode)
    filter_.setNext(child)
    filter_.println(99, "PublicTAG", "HelloWorldMsg", None)
    child.println.assert_called_once_with(99, None, "HelloWorldMsg", None)

def test_no_next_node_is_safe_public():
    filter_ = MessageOnlyLogFilter()
    filter_.println(88, "AnotherTAG", "SomeMessage", None)
    # No exception should be thrown

def test_chained_next_node_public():
    filter_ = MessageOnlyLogFilter()
    chain_child = Mock(spec=LogNode)
    filter_.setNext(chain_child)
    filter_.println(5, "TagChain", "ChainedMsg", RuntimeError("publicChain"))
    chain_child.println.assert_called_once_with(5, None, "ChainedMsg", None)