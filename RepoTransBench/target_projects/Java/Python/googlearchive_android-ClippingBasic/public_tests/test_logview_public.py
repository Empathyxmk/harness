import pytest
from unittest import mock

class LogNode:
    def println(self, priority, tag, msg, tr):
        pass

class DummyActivity:
    def __init__(self):
        self.didRunOnUiThread = False
        self.lastRunnable = None
    def runOnUiThread(self, action):
        self.didRunOnUiThread = True
        self.lastRunnable = action
        action()

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
        if val is None or val == "":
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
def setup():
    yield

def test_append_if_not_null_public():
    dummyActivity = DummyActivity()
    view = LogView(dummyActivity)

    sb = []
    result = view.appendIfNotNull(sb, "xyz", ";")
    assert "".join(result) == "xyz;"
    sb = []
    result = view.appendIfNotNull(sb, None, "~")
    assert "".join(result) == ""
    sb = ["y"]
    result = view.appendIfNotNull(sb, "", "?")
    assert "".join(result) == "y"

def test_get_set_next_public():
    dummyActivity = DummyActivity()
    view = LogView(dummyActivity)
    filter_ = MessageOnlyLogFilter()
    view.setNext(filter_)
    assert view.getNext() == filter_

def test_println_formats_and_runs_runnable_public():
    dummyActivity = DummyActivity()
    view = LogView(dummyActivity)
    next_mock = mock.Mock(spec=LogNode)
    view.setNext(next_mock)

    tr = RuntimeError("pubTest")
    view.println(5, "publicTag", "publicMsg", tr)

    next_mock.println.assert_called_with(5, "publicTag", "publicMsg", tr)
    assert dummyActivity.didRunOnUiThread