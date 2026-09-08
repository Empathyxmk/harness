import pytest

class LogNode:
    def println(self, priority, tag, msg, tr):
        pass

class Log:
    VERBOSE = 2
    WARN = 5
    NONE = -1

class MessageOnlyLogFilter(LogNode):
    def __init__(self, next_node=None):
        self._next = next_node

    def setNext(self, next_node):
        self._next = next_node

    def getNext(self):
        return self._next

    def println(self, priority, tag, msg, tr):
        if self._next:
            self._next.println(Log.NONE, None, msg, None)

class RecordingNode(LogNode):
    def __init__(self):
        self.lastPriority = float('inf')
        self.lastTag = "abc"
        self.lastMsg = "zzz"
        self.lastTr = None

    def println(self, priority, tag, msg, tr):
        self.lastPriority = priority
        self.lastTag = tag
        self.lastMsg = msg
        self.lastTr = tr

@pytest.fixture(autouse=True)
def setup_filter():
    yield

def test_println_filters_to_message_only_public():
    recorder = RecordingNode()
    filter_ = MessageOnlyLogFilter()
    filter_.setNext(recorder)
    filter_.println(Log.WARN, "PUBTAG", "public message", Exception("not seen"))
    assert recorder.lastPriority == Log.NONE
    assert recorder.lastTag is None
    assert recorder.lastMsg == "public message"
    assert recorder.lastTr is None

def test_constructor_with_next_public():
    recorder = RecordingNode()
    f2 = MessageOnlyLogFilter(recorder)
    assert f2.getNext() == recorder

def test_set_and_get_next_public():
    recorder = RecordingNode()
    f3 = MessageOnlyLogFilter()
    f3.setNext(recorder)
    assert f3.getNext() == recorder

def test_null_next_does_nothing_public():
    f4 = MessageOnlyLogFilter()
    # Should not throw
    f4.println(Log.VERBOSE, "v", "pqrs", None)