import math
from d3polygon import polygon_length

def test_length_closed_counterclockwise():
    assert polygon_length([[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]]) == 4

def test_length_closed_clockwise():
    assert polygon_length([[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]) == 4
    result = polygon_length([[1, 1], [3, 2], [2, 3], [1, 1]])
    assert abs(result - (math.sqrt(20) + math.sqrt(2))) < 1e-10

def test_length_open_counterclockwise():
    assert polygon_length([[0, 0], [0, 1], [1, 1], [1, 0]]) == 4

def test_length_open_clockwise():
    assert polygon_length([[0, 0], [1, 0], [1, 1], [0, 1]]) == 4
    result = polygon_length([[1, 1], [3, 2], [2, 3]])
    assert abs(result - (math.sqrt(20) + math.sqrt(2))) < 1e-10