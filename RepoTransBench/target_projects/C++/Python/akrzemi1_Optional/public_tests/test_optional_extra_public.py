import pytest

class DummyPublic:
    def __init__(self, val=123):
        self.val = val

    def __eq__(self, other):
        if isinstance(other, DummyPublic):
            return self.val == other.val
        return False

def test_emplace_and_swap_public():
    class OptionalWrapper:
        def __init__(self):
            self._has_value = False
            self._value = None
        def emplace(self, val=None):
            if val is None:
                self._value = DummyPublic()
            else:
                self._value = DummyPublic(val)
            self._has_value = True
        def swap(self, other):
            self._value, other._value = other._value, self._value
            self._has_value, other._has_value = other._has_value, self._has_value
        def __getattr__(self, name):
            return getattr(self._value, name)
        def __bool__(self):
            return self._has_value

    a, b = OptionalWrapper(), OptionalWrapper()
    a.emplace(321)
    b.emplace(42)
    a.swap(b)
    assert a.val == 42
    assert b.val == 321

def test_emplace_default_public():
    class OptionalWrapper:
        def __init__(self):
            self._has_value = False
            self._value = None
        def emplace(self):
            self._value = DummyPublic()
            self._has_value = True
        def has_value(self):
            return self._has_value
        def __getattr__(self, name):
            return getattr(self._value, name)
        def __bool__(self):
            return self._has_value

    x = OptionalWrapper()
    x.emplace()
    assert x.has_value()
    assert x.val == 123

def test_assign_none_public():
    class OptionalWrapper:
        def __init__(self, val=None):
            self._value = val
            self._has_value = val is not None
        def __bool__(self):
            return self._has_value
        def has_value(self):
            return self._has_value

    op = OptionalWrapper(77)
    op = OptionalWrapper() # simulate "op = nullopt"
    assert not op.has_value()

def test_comparisons_public():
    class OptionalWrapper:
        def __init__(self, val=None):
            self._has_value = val is not None
            self._value = val
        def __eq__(self, other):
            return (self._has_value, self._value) == (other._has_value, other._value)
        def __lt__(self, other):
            if not self._has_value and other._has_value:
                return True
            if self._has_value and not other._has_value:
                return False
            if not self._has_value and not other._has_value:
                return False
            return self._value < other._value
        def __gt__(self, other):
            if self._has_value and not other._has_value:
                return True
            if not self._has_value and other._has_value:
                return False
            if not self._has_value and not other._has_value:
                return False
            return self._value > other._value

    o1 = OptionalWrapper(8)
    o2 = OptionalWrapper(90)
    o3 = OptionalWrapper()  # disengaged
    assert o1 != o2
    assert o1 < o2
    assert o3 < o1
    assert o2 > o1
    assert not (o1 < o1)