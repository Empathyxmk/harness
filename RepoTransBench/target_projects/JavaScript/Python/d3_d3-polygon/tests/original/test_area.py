import math
import pytest
from d3polygon import polygon_area

def test_area_closed_counterclockwise():
    assert polygon_area([[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]]) == 1

def test_area_closed_clockwise():
    assert polygon_area([[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]) == -1
    assert polygon_area([[1, 1], [3, 2], [2, 3], [1, 1]]) == -1.5

def test_area_open_counterclockwise():
    assert polygon_area([[0, 0], [0, 1], [1, 1], [1, 0]]) == 1

def test_area_open_clockwise():
    assert polygon_area([[0, 0], [1, 0], [1, 1], [0, 1]]) == -1
    assert polygon_area([[1, 1], [3, 2], [2, 3]]) == -1.5

def test_area_very_large_polygon():
    stop = int(1e8)
    step = int(1e4)
    points = []
    value = 0
    while value < stop:
        points.append([0, value])
        value += step
    value = 0
    while value < stop:
        points.append([value, stop])
        value += step
    value = stop - step
    while value >= 0:
        points.append([stop, value])
        value -= step
    value = stop - step
    while value >= 0:
        points.append([value, 0])
        value -= step
    assert polygon_area(points) == 1e16 - 5e7