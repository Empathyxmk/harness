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
        if add is not None and add != "":
            sb.append(str(add))
            sb.append(str(delim))
        return sb

    def appendToLog(self, s):
        self.last_appended = s

    def println(self, priority, tag, msg, tr):
        log_str = f"{priority} {tag} {msg}"
        if tr:
            log_str += f" {type(tr).__name__}:{tr}"
        self.appendToLog(log_str)
        if self._next:
            self._next.println(priority, tag, msg, tr)

def test_all_constructors():
    ctx = object()
    attrs = object()
    v1 = LogView(ctx)
    v2 = LogView(ctx, attrs)
    v3 = LogView(ctx, attrs, 2)
    assert v1 is not None
    assert v2 is not None
    assert v3 is not None

def test_append_if_not_null_edge_cases():
    v = LogView(object())
    sb = list("public")
    sb2 = v._appendIfNotNull(sb, "append", "|")
    assert ''.join(sb2) == "publicappend|"

    sb = list("q")
    sb2 = v._appendIfNotNull(sb, "", "|")
    assert ''.join(sb2) == "q"

    sb = []
    sb2 = v._appendIfNotNull(sb, None, ";")
    assert ''.join(sb2) == ""

def test_println_with_public_data():
    v = LogView(object())
    caught = {"val": None}
    def fake_appendToLog(s):
        caught['val'] = s
    v.appendToLog = fake_appendToLog

    v.println(4, "tagPublic1", "msgInfo", None)
    assert "4" in caught['val'] and "tagPublic1" in caught['val'] and "msgInfo" in caught['val']

    v.println(3, "tagPublic2", "msgDebug", Exception("InvalidArg"))
    assert "3" in caught['val'] and "msgDebug" in caught['val'] and "Exception" in caught['val']

    next_node = Mock(spec=LogNode)
    v.setNext(next_node)
    v.println(2, "tagP", "msgP", None)
    assert next_node.println.called

def test_set_get_next_node_public():
    v = LogView(object())
    assert v.getNext() is None
    ln = Mock(spec=LogNode)
    v.setNext(ln)
    assert v.getNext() is ln