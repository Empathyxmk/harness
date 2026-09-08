import pytest

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

def test_context_equals():
    c1 = Context("A", 1)
    c2 = Context("A", 1)
    c3 = Context("B", 2)
    assert c1 == c2
    assert c1 != c3

def test_context_hashcode():
    c1 = Context("A", 1)
    c2 = Context("A", 1)
    assert hash(c1) == hash(c2)

def test_null_context():
    c1 = Context(None, 0)
    c2 = Context(None, 0)
    assert c1 == c2

def test_context_tostring():
    c1 = Context("Method", 5)
    assert "Method" in str(c1)