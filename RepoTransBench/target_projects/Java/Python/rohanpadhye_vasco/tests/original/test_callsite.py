import pytest

class DummyContext:
    def __init__(self, id):
        self.method = "m"
        self.id = id

    def getId(self):
        return self.id

    def __eq__(self, other):
        return isinstance(other, DummyContext) and self.id == other.id

    def __hash__(self):
        return self.id

# Simulate the CallSite class.
class CallSite:
    def __init__(self, calling_context, call_node):
        self.calling_context = calling_context
        self.call_node = call_node

    def __eq__(self, other):
        if not isinstance(other, CallSite):
            return False
        return (self.calling_context == other.calling_context and
                self.call_node == other.call_node)

    def __hash__(self):
        return hash(self.calling_context) * 31 + hash(self.call_node)

    def __lt__(self, other):
        if not isinstance(other, CallSite):
            return NotImplemented
        if self.calling_context.getId() != other.calling_context.getId():
            return self.calling_context.getId() < other.calling_context.getId()
        return self.call_node < other.call_node

    def compareTo(self, other):  # for Java-style comparison
        if self.calling_context.getId() != other.calling_context.getId():
            return self.calling_context.getId() - other.calling_context.getId()
        # Compare by call_node
        if self.call_node == other.call_node:
            return 0
        return -1 if self.call_node < other.call_node else 1

    def getCallingContext(self):
        return self.calling_context

    def getCallNode(self):
        return self.call_node

    def __str__(self):
        return f"CallSite(context={self.calling_context}, node={self.call_node})"

def test_equals_and_hashcode():
    ctx1 = DummyContext(1)
    ctx2 = DummyContext(2)
    cs1 = CallSite(ctx1, "call1")
    cs2 = CallSite(ctx1, "call1")
    cs3 = CallSite(ctx1, "call2")
    cs4 = CallSite(ctx2, "call1")

    assert cs1 == cs2
    assert hash(cs1) == hash(cs2)
    assert cs1 != cs3
    assert cs1 != cs4
    assert cs1 != None
    assert cs1 != "SomeString"

def test_compare_to():
    ctx1 = DummyContext(1)
    ctx2 = DummyContext(4)
    cs1 = CallSite(ctx1, "c1")
    cs2 = CallSite(ctx2, "c1")
    assert cs1.compareTo(cs2) < 0
    assert cs2.compareTo(cs1) > 0
    assert cs1.compareTo(CallSite(ctx1, "c2")) == 0

def test_getters_tostring():
    ctx1 = DummyContext(42)
    cs1 = CallSite(ctx1, "stmtNode")
    assert cs1.getCallingContext() == ctx1
    assert cs1.getCallNode() == "stmtNode"
    s = str(cs1)
    assert "42" in s
    assert "stmtNode" in s