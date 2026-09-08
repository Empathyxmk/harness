# Tests for data abstraction/functional object patterns
class Maybe:
    def __init__(self, value):
        self.value = value
    def is_nothing(self):
        return self.value is None
    def map(self, f):
        if self.is_nothing():
            return Maybe(None)
        else:
            return Maybe(f(self.value))

def test_maybe_just():
    m = Maybe(10)
    assert not m.is_nothing()
    assert m.map(lambda x: x+5).value == 15

def test_maybe_nothing():
    m = Maybe(None)
    assert m.is_nothing()
    assert m.map(lambda x: x+1).is_nothing()