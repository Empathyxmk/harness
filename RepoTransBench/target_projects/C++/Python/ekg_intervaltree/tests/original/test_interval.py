import pytest
from src.interval import Interval

# ---- Existing/Fixed Tests ----

def test_interval_equality_and_inequality():
    i1 = Interval(1, 5, "a")
    i2 = Interval(1, 5, "a")
    i3 = Interval(2, 6, "b")
    assert i1 == i2
    assert i1 != i3

def test_interval_ostream_operator():
    i1 = Interval(1, 5, "a")
    s = str(i1)
    assert "[1, 5]" in s
    assert "val: a" in s

def test_default_constructed_interval():
    i = Interval()
    assert i.start == 0
    assert i.stop == 0
    assert i.value == ""

# ---- New Tests for coverage ----

def test_interval_with_non_default_value():
    i = Interval(10, 15, "foo")
    assert i.start == 10
    assert i.stop == 15
    assert i.value == "foo"

def test_self_assignment_and_copy():
    i1 = Interval(1, 2, "copy")
    i2 = Interval(i1.start, i1.stop, i1.value)
    i1 = i1  # self-assign in Python, does nothing in this context
    assert i1 == i2

def test_assignment_operator():
    i1 = Interval(4, 8, "first")
    i2 = Interval()
    i2 = Interval(i1.start, i1.stop, i1.value)
    assert i2 == i1

def test_different_types_or_values_not_equal():
    i1 = Interval(1, 2, "one")
    i2 = Interval(2, 3, "one")
    i3 = Interval(1, 2, "two")
    assert not (i1 == i2)
    assert not (i1 == i3)

def test_inequality_operator_with_identical_objects_returns_false():
    i1 = Interval(9, 12, "same")
    assert not (i1 != i1)