class CallSite:
    def __init__(self, method, id_):
        self.method = method
        self.id = id_

    def __eq__(self, other):
        return isinstance(other, CallSite) and self.method == other.method and self.id == other.id

    def __hash__(self):
        return hash((self.method, self.id))

    def __str__(self):
        return f"CallSite({self.method!r}, {self.id})"

def test_equals_and_hashcode():
    cs1 = CallSite("foo", 1)
    cs2 = CallSite("foo", 1)
    cs3 = CallSite("bar", 2)

    assert cs1 == cs2
    assert cs1 != cs3
    assert hash(cs1) == hash(cs2)
    assert hash(cs1) != hash(cs3)

def test_to_string():
    cs = CallSite("main", 3)
    s = str(cs)
    assert "main" in s
    assert "3" in s