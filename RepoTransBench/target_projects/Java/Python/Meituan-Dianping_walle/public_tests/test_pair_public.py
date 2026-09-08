class Pair:
    def __init__(self, first, second):
        self.first = first
        self.second = second

    @staticmethod
    def of(first, second):
        return Pair(first, second)

    def getFirst(self):
        return self.first

    def getSecond(self):
        return self.second

    def __eq__(self, other):
        if not isinstance(other, Pair):
            return False
        return self.first == other.first and self.second == other.second

    def __hash__(self):
        return hash((self.first, self.second))

def test_of_and_getters_public():
    pair = Pair.of(12345, "hello")
    assert pair.getFirst() == 12345
    assert pair.getSecond() == "hello"

    pair2 = Pair.of(3.14, 2.71)
    assert pair2.getFirst() == 3.14
    assert pair2.getSecond() == 2.71

def test_equals_and_hash_code_public():
    a = Pair.of("A", "B")
    b = Pair.of("A", "B")
    assert a == b
    assert hash(a) == hash(b)

    c = Pair.of("A", "C")
    assert a != c

    d = Pair.of(None, "B")
    e = Pair.of(None, "B")
    assert d == e
    assert hash(d) == hash(e)