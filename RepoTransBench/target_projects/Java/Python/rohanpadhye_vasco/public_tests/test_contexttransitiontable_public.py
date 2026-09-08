class Context:
    def __init__(self, method, id_):
        self.method = method
        self.id = id_

    def __eq__(self, other):
        return isinstance(other, Context) and self.method == other.method and self.id == other.id

    def __hash__(self):
        return hash((self.method, self.id))

class ContextTransitionTable:
    def __init__(self):
        self.transitions = {}

    def put(self, base, edge, next_):
        self.transitions.setdefault((base, edge), next_)

    def containsTransition(self, base, edge):
        return (base, edge) in self.transitions

    def getTarget(self, base, edge):
        return self.transitions.get((base, edge), None)

def test_different_transition_table():
    table = ContextTransitionTable()
    base = Context("foo", 123)
    next_ = Context("bar", 321)
    table.put(base, "edge", next_)

    assert table.containsTransition(base, "edge")
    assert not table.containsTransition(base, "nonexistent")
    assert table.getTarget(base, "edge") == next_
    assert table.getTarget(base, "noTransition") is None

def test_null_base_context_table():
    table = ContextTransitionTable()
    base = Context(None, -1)
    next_ = Context("baz", 888)
    table.put(base, "x", next_)

    assert table.containsTransition(base, "x")
    assert table.getTarget(base, "x") == next_