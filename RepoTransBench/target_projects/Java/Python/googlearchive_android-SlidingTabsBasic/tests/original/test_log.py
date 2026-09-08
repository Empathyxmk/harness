import pytest
from unittest.mock import Mock, call, ANY

class LogNode:
    def println(self, priority, tag, msg, tr):
        pass

class Log:
    VERBOSE = 2
    DEBUG = 3
    INFO = 4
    WARN = 5
    ERROR = 6
    ASSERT = 7
    NONE = 0

    _log_node = None

    @classmethod
    def setLogNode(cls, node):
        cls._log_node = node

    @classmethod
    def getLogNode(cls):
        return cls._log_node

    @classmethod
    def println(cls, priority, tag, msg, tr=None):
        if cls._log_node:
            cls._log_node.println(priority, tag, msg, tr)

    @classmethod
    def v(cls, tag, msg, tr=None):
        cls.println(cls.VERBOSE, tag, msg, tr)

    @classmethod
    def d(cls, tag, msg, tr=None):
        cls.println(cls.DEBUG, tag, msg, tr)

    @classmethod
    def i(cls, tag, msg, tr=None):
        cls.println(cls.INFO, tag, msg, tr)

    @classmethod
    def w(cls, tag, msg, tr=None):
        cls.println(cls.WARN, tag, msg, tr)

    @classmethod
    def e(cls, tag, msg, tr=None):
        cls.println(cls.ERROR, tag, msg, tr)

    @classmethod
    def wtf(cls, tag, msg, tr=None):
        cls.println(cls.ASSERT, tag, msg, tr)

@pytest.fixture(autouse=True)
def clear_lognode():
    Log.setLogNode(None)
    yield
    Log.setLogNode(None)

@pytest.fixture
def mock_node():
    node = Mock(spec=LogNode)
    Log.setLogNode(node)
    return node

def test_set_and_get_lognode(mock_node):
    assert Log.getLogNode() is mock_node

def test_println_calls_node(mock_node):
    Log.println(Log.DEBUG, 'TAG', 'msg', None)
    mock_node.println.assert_any_call(Log.DEBUG, 'TAG', 'msg', None)

    Log.println(Log.INFO, 'TAG2', 'msg2')
    mock_node.println.assert_any_call(Log.INFO, 'TAG2', 'msg2', None)

def test_verbosity_delegates(mock_node):
    Log.v("V", "verbose")
    mock_node.println.assert_any_call(Log.VERBOSE, "V", "verbose", None)

    Log.v("V2", "verbose2", Exception("err"))
    mock_node.println.assert_any_call(Log.VERBOSE, "V2", "verbose2", ANY)

def test_debug_delegates(mock_node):
    Log.d("D", "debug")
    mock_node.println.assert_any_call(Log.DEBUG, "D", "debug", None)

    Log.d("D2", "debug2", Exception("err"))
    mock_node.println.assert_any_call(Log.DEBUG, "D2", "debug2", ANY)

def test_info_delegates(mock_node):
    Log.i("I", "info")
    mock_node.println.assert_any_call(Log.INFO, "I", "info", None)

    Log.i("I2", "info2", Exception("err"))
    mock_node.println.assert_any_call(Log.INFO, "I2", "info2", ANY)

def test_warn_delegates(mock_node):
    Log.w("W", "warn")
    mock_node.println.assert_any_call(Log.WARN, "W", "warn", None)

    Log.w("W2", "warn2", Exception("err"))
    mock_node.println.assert_any_call(Log.WARN, "W2", "warn2", ANY)

def test_error_delegates(mock_node):
    Log.e("E", "error")
    mock_node.println.assert_any_call(Log.ERROR, "E", "error", None)

    Log.e("E2", "error2", Exception("err"))
    mock_node.println.assert_any_call(Log.ERROR, "E2", "error2", ANY)

def test_wtf_delegates(mock_node):
    Log.wtf("T", "assert")
    mock_node.println.assert_any_call(Log.ASSERT, "T", "assert", None)

    Log.wtf("T2", "assert2", Exception("err"))
    mock_node.println.assert_any_call(Log.ASSERT, "T2", "assert2", ANY)

def test_no_node_does_not_crash():
    Log.setLogNode(None)
    # Should not throw
    Log.d("TAG", "Should do nothing")