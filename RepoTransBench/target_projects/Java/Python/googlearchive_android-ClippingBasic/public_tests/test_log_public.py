import pytest

class TestLogNode:
    def __init__(self):
        self.priority = None
        self.tag = None
        self.msg = None
        self.tr = None

    def println(self, priority, tag, msg, tr):
        self.priority = priority
        self.tag = tag
        self.msg = msg
        self.tr = tr

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
    NONE = -1

    _node = None

    @classmethod
    def setLogNode(cls, node):
        cls._node = node

    @classmethod
    def getLogNode(cls):
        return cls._node

    @classmethod
    def println(cls, priority, tag, msg, tr=None):
        if cls._node is not None:
            cls._node.println(priority, tag, msg, tr)

    @classmethod
    def v(cls, tag, msg):
        cls.println(cls.VERBOSE, tag, msg, None)

    @classmethod
    def d(cls, tag, msg):
        cls.println(cls.DEBUG, tag, msg, None)

    @classmethod
    def i(cls, tag, msg):
        cls.println(cls.INFO, tag, msg, None)

    @classmethod
    def w(cls, tag, msg):
        cls.println(cls.WARN, tag, msg, None)

    @classmethod
    def e(cls, tag, msg, tr=None):
        cls.println(cls.ERROR, tag, msg, tr)

    @classmethod
    def wtf(cls, tag, msg):
        cls.println(cls.ASSERT, tag, msg, None)

@pytest.fixture(autouse=True)
def setUp_and_tearDown():
    # Each test gets a self-contained test node and log is reset
    testNode = TestLogNode()
    Log.setLogNode(testNode)
    yield
    Log.setLogNode(None)

def test_set_and_get_log_node_public():
    testNode = TestLogNode()
    Log.setLogNode(testNode)
    assert Log.getLogNode() == testNode

def test_println_with_throwable_public():
    testNode = TestLogNode()
    Log.setLogNode(testNode)
    tr = ValueError("PublicException")
    Log.println(Log.ERROR, "PUB", "public_msg", tr)
    assert testNode.priority == Log.ERROR
    assert testNode.tag == "PUB"
    assert testNode.msg == "public_msg"
    assert testNode.tr == tr

def test_println_without_throwable_public():
    testNode = TestLogNode()
    Log.setLogNode(testNode)
    Log.println(Log.WARN, "PUB2", "public_msg2")
    assert testNode.priority == Log.WARN
    assert testNode.tag == "PUB2"
    assert testNode.msg == "public_msg2"
    assert testNode.tr is None

def test_level_shortcuts_public():
    testNode = TestLogNode()
    Log.setLogNode(testNode)
    Log.v("PUBv", "visible")
    assert testNode.priority == Log.VERBOSE
    Log.d("PUBd", "debugging")
    assert testNode.priority == Log.DEBUG
    Log.i("PUBi", "information")
    assert testNode.priority == Log.INFO
    Log.w("PUBw", "warning")
    assert testNode.priority == Log.WARN
    Log.e("PUBe", "error occurred", Exception())
    assert testNode.priority == Log.ERROR
    Log.wtf("PUBa", "assertion")
    assert testNode.priority == Log.ASSERT

def test_no_log_node_set_public():
    Log.setLogNode(None)
    # Should not throw even if node is null
    Log.println(Log.INFO, "PUB", "public_msg", None)