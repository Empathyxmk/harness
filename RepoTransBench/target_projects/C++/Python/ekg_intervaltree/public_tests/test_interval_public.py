import pytest
from src.interval import Interval

# ---- Public Tests (different data from private) ----

def test_interval_equality_and_inequality_public():
    i1 = Interval(3, 7, "b")
    i2 = Interval(3, 7, "b")
    i3 = Interval(4, 9, "c")
    assert i1 == i2
    assert i1 != i3

def test_interval_ostream_operator_public():
    i1 = Interval(8, 16, "hello")
    s = str(i1)
    assert "[8, 16]" in s
    assert "val: hello" in s

def test_default_constructed_interval_public():
    i = Interval()
    assert i.start == 0
    assert i.stop == 0
    assert i.value == ""

def test_interval_with_non_default_value_public():
    i = Interval(25, 30, "bar")
    assert i.start == 25
    assert i.stop == 30
    assert i.value == "bar"

def test_self_assignment_and_copy_public():
    i1 = Interval(5, 10, "clone")
    i2 = Interval(i1.start, i1.stop, i1.value)
    i1 = i1  # self-assign, no-op
    assert i1 == i2

def test_assignment_operator_public():
    i1 = Interval(11, 14, "second")
    i2 = Interval()
    i2 = Interval(i1.start, i1.stop, i1.value)
    assert i2 == i1

def test_different_types_or_values_not_equal_public():
    i1 = Interval(6, 12, "alpha")
    i2 = Interval(7, 12, "alpha")
    i3 = Interval(6, 12, "beta")
    assert not (i1 == i2)
    assert not (i1 == i3)

def test_inequality_operator_with_identical_objects_returns_false_public():
    i1 = Interval(20, 22, "identical")
    assert not (i1 != i1)