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

def test_of_getters():
    pair = Pair.of("hello", 42)
    assert pair.getFirst() == "hello"
    assert pair.getSecond() == 42

def test_equals_hash_code_same_object():
    pair = Pair.of("foo", 123)
    assert pair == pair
    assert hash(pair) == hash(pair)

def test_equals_hash_code_equal_pairs():
    pair1 = Pair.of("a", 1)
    pair2 = Pair.of("a", 1)
    assert pair1 == pair2
    assert pair2 == pair1
    assert hash(pair1) == hash(pair2)

def test_equals_not_equal_by_first():
    pair1 = Pair.of("a", 1)
    pair2 = Pair.of("b", 1)
    assert not (pair1 == pair2)
    assert not (pair2 == pair1)

def test_equals_not_equal_by_second():
    pair1 = Pair.of("a", 1)
    pair2 = Pair.of("a", 2)
    assert not (pair1 == pair2)
    assert not (pair2 == pair1)

def test_equals_null_object():
    pair = Pair.of("x", 10)
    assert not (pair == None)

def test_equals_different_class():
    pair = Pair.of("x", 10)
    assert not (pair == "not a pair")

def test_equals_null_fields():
    p1 = Pair.of(None, None)
    p2 = Pair.of(None, None)
    assert p1 == p2
    assert hash(p1) == hash(p2)

def test_equals_null_first_different_second():
    p1 = Pair.of(None, 10)
    p2 = Pair.of(None, 11)
    assert not (p1 == p2)

def test_equals_different_first_null_second():
    p1 = Pair.of("x", None)
    p2 = Pair.of("y", None)
    assert not (p1 == p2)

def test_equals_null_first_nonnull_other():
    p1 = Pair.of(None, 1)
    p2 = Pair.of("z", 1)
    assert not (p1 == p2)

def test_equals_nonnull_first_null_other():
    p1 = Pair.of("z", 1)
    p2 = Pair.of(None, 1)
    assert not (p1 == p2)