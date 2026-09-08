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

def test_set_and_get_lognode_public(mock_node):
    assert Log.getLogNode() is mock_node

def test_println_calls_node_with_different_values(mock_node):
    Log.println(Log.INFO, 'PUB_TAG', 'publicMsg', None)
    mock_node.println.assert_any_call(Log.INFO, 'PUB_TAG', 'publicMsg', None)

    Log.println(Log.WARN, 'PUB_TAG_WARN', 'warnMsg')
    mock_node.println.assert_any_call(Log.WARN, 'PUB_TAG_WARN', 'warnMsg', None)

def test_verbose_delegates_with_different_input(mock_node):
    Log.v("VerboseTag", "verbMsg")
    mock_node.println.assert_any_call(Log.VERBOSE, "VerboseTag", "verbMsg", None)

    Log.v("VerbTag2", "verbMsg2", Exception("public"))
    mock_node.println.assert_any_call(Log.VERBOSE, "VerbTag2", "verbMsg2", ANY)

def test_debug_delegates_with_different_input(mock_node):
    Log.d("DebugTag", "debugMessage")
    mock_node.println.assert_any_call(Log.DEBUG, "DebugTag", "debugMessage", None)

    Log.d("DebugTag2", "debugMessage2", Exception("failure"))
    mock_node.println.assert_any_call(Log.DEBUG, "DebugTag2", "debugMessage2", ANY)

def test_info_delegates_with_public_data(mock_node):
    Log.i("InfoTag", "infoMsg1")
    mock_node.println.assert_any_call(Log.INFO, "InfoTag", "infoMsg1", None)

    Log.i("InfoTag2", "infoMsg2", Exception("infoNull"))
    mock_node.println.assert_any_call(Log.INFO, "InfoTag2", "infoMsg2", ANY)

def test_warn_delegates_public(mock_node):
    Log.w("WarnTag", "warnMsg1")
    mock_node.println.assert_any_call(Log.WARN, "WarnTag", "warnMsg1", None)

    Log.w("WarnTag2", "warnMsg2", Exception("warnArith"))
    mock_node.println.assert_any_call(Log.WARN, "WarnTag2", "warnMsg2", ANY)

def test_error_delegates_public(mock_node):
    Log.e("ErrorTag", "errorMsg1")
    mock_node.println.assert_any_call(Log.ERROR, "ErrorTag", "errorMsg1", None)

    Log.e("ErrorTag2", "errorMsg2", Exception("publicError"))
    mock_node.println.assert_any_call(Log.ERROR, "ErrorTag2", "errorMsg2", ANY)

def test_wtf_delegates_with_different_data(mock_node):
    Log.wtf("AssertT", "assertMsg")
    mock_node.println.assert_any_call(Log.ASSERT, "AssertT", "assertMsg", None)

    Log.wtf("AssertT2", "assertMsg2", Exception("assertThrowable"))
    mock_node.println.assert_any_call(Log.ASSERT, "AssertT2", "assertMsg2", ANY)

def test_no_node_safe_on_null_public():
    Log.setLogNode(None)
    Log.i("SafeTAG", "ShouldBeSafe")