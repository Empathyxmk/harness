import pytest

from typing import Optional

# Simulate std::experimental::optional with Python's Optional + custom helpers for some behaviors

class BadOptionalAccess(Exception):
    pass

class OptionalWrapper:
    def __init__(self, value=None):
        self._engaged = value is not None
        self._value = value

    def __bool__(self):
        return self._engaged

    def has_value(self):
        return self._engaged

    def value(self):
        if not self._engaged:
            raise BadOptionalAccess("bad optional access")
        return self._value

    def reset(self):
        self._engaged = False
        self._value = None

    def emplace(self, value=None):
        self._engaged = True
        if value is not None:
            self._value = value
        else:
            # For str, int, etc: default to constructor
            if hasattr(self._value, '__class__'):
                self._value = self._value.__class__()
            else:
                self._value = None

    def __eq__(self, other):
        if not isinstance(other, OptionalWrapper):
            return False
        if not self._engaged and not other._engaged:
            return True
        return self._engaged == other._engaged and self._value == other._value

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        if not self._engaged and other._engaged:
            return True
        if self._engaged and not other._engaged:
            return False
        if not self._engaged and not other._engaged:
            return False
        return self._value < other._value

    def __gt__(self, other):
        if self._engaged and not other._engaged:
            return True
        if not self._engaged and other._engaged:
            return False
        if not self._engaged and not other._engaged:
            return False
        return self._value > other._value

    def __le__(self, other):
        return self == other or self < other

    def __ge__(self, other):
        return self == other or self > other

    def swap(self, other):
        self._engaged, other._engaged = other._engaged, self._engaged
        self._value, other._value = other._value, self._value

    def __call__(self):
        return self.value()

    def __getattr__(self, name):
        return getattr(self.value(), name)

    def __setitem__(self, key, value):
        self._value[key] = value

    def __getitem__(self, key):
        return self._value[key]

    def __repr__(self):
        if self._engaged:
            return f"OptionalWrapper({self._value!r})"
        else:
            return "OptionalWrapper(None)"

    def __iter__(self):
        if self._engaged:
            yield self._value

    def __deref__(self):
        return self.value()

    # Used for *o in C++: In python, .value() is what you want
    def __star__(self):
        return self.value()


def swap(a, b):
    a.swap(b)


def test_throws_on_bad_access():
    o = OptionalWrapper()
    assert not o
    with pytest.raises(BadOptionalAccess):
        _ = o.value()
    s = OptionalWrapper()
    assert not s.has_value()
    with pytest.raises(BadOptionalAccess):
        _ = s.value()

def test_reset_and_emplace():
    o = OptionalWrapper(55)
    assert o
    assert o.value() == 55
    o.reset()
    assert not o
    o.emplace(100)
    assert o.has_value()
    assert o.value() == 100

def test_dereference_operator():
    o = OptionalWrapper(10)
    assert o.value() == 10
    # In python, we use .value() since no operator*

def test_comparisons():
    o1 = OptionalWrapper(1)
    o2 = OptionalWrapper(2)
    o3 = OptionalWrapper(1)
    o0 = OptionalWrapper()
    assert o1 == o3
    assert o1 != o2
    assert o0 < o1
    assert o1 > o0
    assert o0 <= o1
    assert o2 >= o1

def test_swap_for_optionals():
    a = OptionalWrapper("hi")
    b = OptionalWrapper("bye")
    swap(a, b)
    assert a.value() == "bye"
    assert b.value() == "hi"

def test_in_place():
    # C++: in_place pair<int,int>(3,4) --> python: tuple
    p = OptionalWrapper((3, 4))
    assert p.value()[0] == 3
    assert p.value()[1] == 4

def test_optional_reference():
    # In python, reference = mutable type or object
    class RefObj:
        def __init__(self, val):
            self.value = val
    x = RefObj(77)
    ref = OptionalWrapper(x)
    assert ref
    ref.value().value = 99
    assert x.value == 99
    rx = ref.value()
    rx.value = 11
    assert x.value == 11

def test_assign_none():
    o = OptionalWrapper(5)
    o = OptionalWrapper()  # simulate o = nullopt
    assert not o.has_value()

def test_copy_assign_disengaged():
    a = OptionalWrapper()
    b = OptionalWrapper(8)
    b = OptionalWrapper(a._value if a.has_value() else None)
    assert not b.has_value()

def test_emplace_default():
    class DummyStr:
        def __init__(self, v=""):
            self.value = v
        def __eq__(self, other):
            if isinstance(other, DummyStr):
                return self.value == other.value
            elif isinstance(other, str):
                return self.value == other
            return False
    o = OptionalWrapper()
    o._value = DummyStr()
    o.emplace()
    assert o.has_value()
    assert o.value() == ""