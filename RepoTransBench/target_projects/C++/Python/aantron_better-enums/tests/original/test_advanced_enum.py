import pytest
from enum import Enum, unique

@unique
class Shape(Enum):
    CIRCLE = 10
    SQUARE = 15
    TRIANGLE = -5

    @classmethod
    def _from_string_nothrow(cls, name):
        try:
            return cls[name]
        except KeyError:
            return None

    def _to_string(self):
        return self.name

    class _enumerated(Enum):
        CIRCLE = 10
        SQUARE = 15
        TRIANGLE = -5

def test_underlying_values():
    s_circle = Shape.CIRCLE
    s_square = Shape.SQUARE
    s_triangle = Shape.TRIANGLE

    assert s_circle.value == 10
    assert s_square.value == 15
    assert s_triangle.value == -5

def test_switch():
    s = Shape.SQUARE
    val = -1
    if s == Shape.CIRCLE:
        val = 1
    elif s == Shape.SQUARE:
        val = 2
    elif s == Shape.TRIANGLE:
        val = 3
    assert val == 2

def test_fail_from_string():
    sh = Shape._from_string_nothrow("NOTASHAPE")
    assert sh is None

def test_name_and_compare():
    s = Shape.CIRCLE
    assert s._to_string() == "CIRCLE"
    assert s == Shape(Shape.CIRCLE)