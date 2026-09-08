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

def test_public_maybe_with_value():
    m = Maybe(3)
    n = m.map(lambda x: x*10)
    assert not n.is_nothing()
    assert n.value == 30

def test_public_maybe_without_value():
    m = Maybe(None)
    n = m.map(lambda x: x+1)
    assert n.is_nothing()