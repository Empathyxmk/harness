class Context:
    def __init__(self, method, id_):
        self.method = method
        self.id = id_
    def __eq__(self, other):
        return isinstance(other, Context) and self.method == other.method and self.id == other.id
    def __hash__(self):
        return hash((self.method, self.id))
    def __str__(self):
        return f"Context({self.method!r}, {self.id})"

def test_context_equals_different():
    c1 = Context("X", 9)
    c2 = Context("X", 9)
    c3 = Context("Y", 20)
    assert c1 == c2
    assert c1 != c3

def test_context_hash_code_different():
    c1 = Context("X", 9)
    c2 = Context("X", 9)
    assert hash(c1) == hash(c2)

def test_null_context_different():
    c1 = Context(None, 42)
    c2 = Context(None, 42)
    assert c1 == c2

def test_context_tostring_different():
    c1 = Context("DifferentMethod", 99)
    assert "DifferentMethod" in str(c1)