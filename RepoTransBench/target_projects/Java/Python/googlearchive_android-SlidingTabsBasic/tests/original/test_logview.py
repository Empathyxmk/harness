import pytest
from unittest.mock import Mock, call, ANY

class LogNode:
    def println(self, priority, tag, msg, tr):
        pass

class LogView:
    def __init__(self, context, attrs=None, def_style=0):
        self.context = context
        self.attrs = attrs
        self.def_style = def_style
        self._next = None

    def setNext(self, node):
        self._next = node

    def getNext(self):
        return self._next

    def _appendIfNotNull(self, sb, add, delim):
        if add is not None and add != '':
            sb.append(str(add))
            sb.append(str(delim))
        return sb

    def appendToLog(self, s):
        # Would normally append to text buffer.
        self.last_appended = s

    def println(self, priority, tag, msg, tr):
        log_str = f"{priority} {tag} {msg}"
        if tr:
            log_str += f" {type(tr).__name__}:{tr}"
        self.appendToLog(log_str)
        if self._next:
            self._next.println(priority, tag, msg, tr)

def test_constructors():
    ctx = object()
    attrs = object()
    v1 = LogView(ctx)
    v2 = LogView(ctx, attrs)
    v3 = LogView(ctx, attrs, 1)
    assert v1 is not None
    assert v2 is not None
    assert v3 is not None

def test_append_if_not_null_behavior():
    v = LogView(object())
    sb = []
    def make_sb(val):
        return [c for c in val]
    def get_str(sb):
        return ''.join(sb)
    sb = list("start")
    sb2 = v._appendIfNotNull(sb, "add", ",")
    assert ''.join(sb2) == "startadd,"

    sb = list("x")
    sb2 = v._appendIfNotNull(sb, "", ",")
    assert ''.join(sb2) == "x"

    sb = []
    sb2 = v._appendIfNotNull(sb, None, "|")
    assert ''.join(sb2) == ""

def test_println_formats_and_appends():
    v = LogView(object())
    caught = {"val": None}
    def fake_appendToLog(s):
        caught['val'] = s
    v.appendToLog = fake_appendToLog

    v.println(5, "tag1", "msg1", None)
    assert "5" in caught['val'] and "tag1" in caught['val'] and "msg1" in caught['val']

    v.println(6, "tag2", "msg2", RuntimeError("Test"))
    assert "6" in caught['val'] and "msg2" in caught['val'] and "RuntimeError" in caught['val']

    # Test mNext
    next_node = Mock(spec=LogNode)
    v.setNext(next_node)
    v.println(4, "tagx", "msgx", None)
    assert next_node.println.called

def test_set_and_get_next():
    v = LogView(object())
    assert v.getNext() is None
    ln = Mock(spec=LogNode)
    v.setNext(ln)
    assert v.getNext() is ln