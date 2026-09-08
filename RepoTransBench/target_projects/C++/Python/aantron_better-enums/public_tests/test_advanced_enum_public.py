import pytest
from enum import Enum, unique

@unique
class Direction(Enum):
    NORTH = 2
    EAST = 5
    SOUTH = -8

    @classmethod
    def _from_string_nothrow(cls, name):
        try:
            return cls[name]
        except KeyError:
            return None

    def _to_string(self):
        return self.name

    class _enumerated(Enum):
        NORTH = 2
        EAST = 5
        SOUTH = -8

def test_underlying_values():
    d_north = Direction.NORTH
    d_east = Direction.EAST
    d_south = Direction.SOUTH

    assert d_north.value == 2
    assert d_east.value == 5
    assert d_south.value == -8

def test_switch():
    d = Direction.EAST
    val = -1
    if d == Direction.NORTH:
        val = 10
    elif d == Direction.EAST:
        val = 20
    elif d == Direction.SOUTH:
        val = 30
    assert val == 20

def test_fail_from_string():
    dir = Direction._from_string_nothrow("UPWARD")
    assert dir is None

def test_name_and_compare():
    d = Direction.SOUTH
    assert d._to_string() == "SOUTH"
    assert d == Direction(Direction.SOUTH)