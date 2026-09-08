import pytest
from d3polygon import polygon_centroid

def test_centroid_public_closed_counterclockwise():
    result = polygon_centroid([[2, 2], [2, 4], [6, 4], [6, 2], [2, 2]])
    assert pytest.approx(result[0], 0.000001) == 4
    assert pytest.approx(result[1], 0.000001) == 3

def test_centroid_public_closed_clockwise():
    result = polygon_centroid([[2, 4], [4, 7], [7, 2], [2, 4]])
    assert pytest.approx(result[0], 1e-6) == 4.333333333333333
    assert pytest.approx(result[1], 1e-6) == 4.333333333333333

def test_centroid_public_open_counterclockwise():
    points = [[0, 0], [1, 3], [4, 4], [6, 1], [3, -2]]
    result = polygon_centroid(points)
    assert pytest.approx(result[0], 1e-6) == 2.6027397260273974
    assert pytest.approx(result[1], 1e-6) == 1.0289855072463768

def test_centroid_public_open_clockwise():
    points = [[4, 0], [8, 4], [4, 8], [0, 4]]
    result = polygon_centroid(points)
    assert pytest.approx(result[0], 1e-6) == 4
    assert pytest.approx(result[1], 1e-6) == 4

def test_centroid_public_large_polygon():
    stop = int(5e7)
    step = int(5e3)
    points = []
    value = 0
    while value < stop:
        points.append([2, value])
        value += step
    value = 0
    while value < stop:
        points.append([value + 2, stop])
        value += step
    value = stop - step
    while value >= 0:
        points.append([stop + 2, value])
        value -= step
    value = stop - step
    while value >= 0:
        points.append([value + 2, 0])
        value -= step
    result = polygon_centroid(points)
    assert pytest.approx(result[0], 1e-6) == stop / 2 + 2
    assert pytest.approx(result[1], 1e-6) == stop / 2