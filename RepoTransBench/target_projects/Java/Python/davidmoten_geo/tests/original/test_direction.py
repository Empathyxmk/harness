import pytest
from enum import Enum

class Direction(Enum):
    TOP = 1
    BOTTOM = 2
    LEFT = 3
    RIGHT = 4

    def opposite(self):
        return {
            Direction.TOP: Direction.BOTTOM,
            Direction.BOTTOM: Direction.TOP,
            Direction.RIGHT: Direction.LEFT,
            Direction.LEFT: Direction.RIGHT
        }[self]

def test_opposite():
    assert Direction.TOP.opposite() == Direction.BOTTOM
    assert Direction.BOTTOM.opposite() == Direction.TOP
    assert Direction.RIGHT.opposite() == Direction.LEFT
    assert Direction.LEFT.opposite() == Direction.RIGHT