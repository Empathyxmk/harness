import pytest
from d3polygon import polygon_contains

def test_contains_closed_counterclockwise():
    assert polygon_contains([[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]], [0.5, 0.5]) is True
    assert polygon_contains([[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]], [1.5, 0.5]) is False
    assert polygon_contains([[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]], [-0.5, 0.5]) is False
    assert polygon_contains([[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]], [0.5, 1.5]) is False
    assert polygon_contains([[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]], [0.5, -0.5]) is False

def test_contains_closed_clockwise():
    assert polygon_contains([[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]], [0.5, 0.5]) is True
    assert polygon_contains([[1, 1], [3, 2], [2, 3], [1, 1]], [1.5, 1.5]) is True

def test_contains_open_counterclockwise():
    assert polygon_contains([[0, 0], [0, 1], [1, 1], [1, 0]], [0.5, 0.5]) is True

def test_contains_open_clockwise():
    assert polygon_contains([[0, 0], [1, 0], [1, 1], [0, 1]], [0.5, 0.5]) is True
    assert polygon_contains([[1, 1], [3, 2], [2, 3]], [1.5, 1.5]) is True