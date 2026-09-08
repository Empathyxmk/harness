class ContextTransitionTable:
    def __init__(self):
        self.transitions = {}

    def put(self, foo, x, y):
        self.transitions.setdefault((foo, x), set()).add(y)

    def get(self, foo, x):
        return self.transitions.get((foo, x), set())

def test_put_and_get_context_transition():
    table = ContextTransitionTable()
    table.put("foo", 1, 2)
    table.put("foo", 1, 3)
    assert 2 in table.get("foo", 1)
    assert 3 in table.get("foo", 1)

def test_empty():
    table = ContextTransitionTable()
    assert not table.get("bar", 42)