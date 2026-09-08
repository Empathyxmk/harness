import pytest
from unittest import mock

# ==== Stubs for LogNode, LogView, MessageOnlyLogFilter ====
class LogNode:
    def println(self, priority, tag, msg, tr):
        pass

class MessageOnlyLogFilter(LogNode):
    def __init__(self, next_node=None):
        self._next = next_node

    def setNext(self, next_node):
        self._next = next_node

    def getNext(self):
        return self._next

    def println(self, priority, tag, msg, tr):
        if self._next:
            self._next.println(priority, tag, msg, tr)

# Dummy Activity and "android" framework stubs
class DummyActivity:
    def __init__(self):
        self.didRunOnUiThread = False
        self.lastRunnable = None

    def runOnUiThread(self, action):
        self.didRunOnUiThread = True
        self.lastRunnable = action
        action()

class LogView(LogNode):
    def __init__(self, context):
        self.context = context
        self._next = None
        self.text = ""
    def setNext(self, next_node):
        self._next = next_node
    def getNext(self):
        return self._next

    def appendIfNotNull(self, sb, val, delimiter):
        if val is None:
            return sb
        if val == "":
            return sb
        sb.append(val)
        if len(delimiter) > 0:
            sb.append(delimiter)
        return sb

    def println(self, priority, tag, msg, tr):
        def add_text():
            self.text += (str(msg) if msg is not None else "")
            if self._next:
                self._next.println(priority, tag, msg, tr)
        if hasattr(self.context, "runOnUiThread"):
            self.context.runOnUiThread(add_text)
        else:
            add_text()

@pytest.fixture(autouse=True)
def setUp_and_tearDown():
    # Each test gets a fresh DummyActivity
    yield

def test_append_if_not_null_behavior():
    dummyActivity = DummyActivity()
    view = LogView(dummyActivity)

    sb = []
    result = view.appendIfNotNull(sb, "abc", ",")
    assert "".join(result) == "abc,"
    sb = []
    result = view.appendIfNotNull(sb, None, "|")
    assert "".join(result) == ""
    sb = ["x"]
    result = view.appendIfNotNull(sb, "", "|")
    assert "".join(result) == "x"

def test_get_set_next():
    dummyActivity = DummyActivity()
    view = LogView(dummyActivity)
    filter_ = MessageOnlyLogFilter()
    view.setNext(filter_)
    assert view.getNext() == filter_

def test_println_formats_and_runs_runnable():
    dummyActivity = DummyActivity()
    view = LogView(dummyActivity)
    next_mock = mock.Mock(spec=LogNode)
    view.setNext(next_mock)

    tr = Exception("e")
    view.println(4, "tag", "msg", tr)

    # Verify that the next LogNode is called with the same params
    next_mock.println.assert_called_with(4, "tag", "msg", tr)
    assert dummyActivity.didRunOnUiThread
    # There should not be an exception