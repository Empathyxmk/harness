import pytest
from src.optional_lite import Optional, nullopt

class NoCopyNoMove:
    def __init__(self):
        self.value = 1234
    def __copy__(self):
        raise RuntimeError("Copy not allowed")
    def __deepcopy__(self, memo):
        raise RuntimeError("DeepCopy not allowed")
    def __setattr__(self, k, v):
        object.__setattr__(self, k, v)


def test_nullopt_construct_and_assign():
    a = Optional(nullopt)
    assert not a
    a = Optional(4)
    assert a
    a = Optional(nullopt)
    assert not a

def test_value_or():
    s = Optional()
    assert s.value_or("fallback") == "fallback"
    s = Optional("abc")
    assert s.value_or("fallback") == "abc"

def test_emplace_reset():
    o = Optional()
    o.emplace(42)
    assert o.has_value()
    o.reset()
    assert not o

def test_move_optional():
    # Python assignment is reference; "move" makes less sense, but simulate
    a = Optional("foo")
    # In C++, b receives ownership; in Python, just clone value logic
    b = Optional(a.value() if a.has_value() else nullopt)
    assert b and b.value() == "foo"

def test_bad_optional_access():
    empty = Optional()
    with pytest.raises(ValueError):
        empty.value()

def test_no_copy_no_move_type():
    n = Optional()
    n.emplace(NoCopyNoMove())
    assert n.value().value == 1234