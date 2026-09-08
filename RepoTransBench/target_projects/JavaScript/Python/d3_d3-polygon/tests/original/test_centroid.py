import pytest
from d3polygon import polygon_centroid

def test_centroid_closed_counterclockwise():
    res = polygon_centroid([[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]])
    assert pytest.approx(res[0], 0.000001) == 0.5
    assert pytest.approx(res[1], 0.000001) == 0.5

def test_centroid_closed_clockwise():
    res1 = polygon_centroid([[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]])
    assert pytest.approx(res1[0], 0.000001) == 0.5
    assert pytest.approx(res1[1], 0.000001) == 0.5

    res2 = polygon_centroid([[1, 1], [3, 2], [2, 3], [1, 1]])
    assert pytest.approx(res2[0], 0.000001) == 2
    assert pytest.approx(res2[1], 0.000001) == 2

def test_centroid_open_counterclockwise():
    res = polygon_centroid([[0, 0], [0, 1], [1, 1], [1, 0]])
    assert pytest.approx(res[0], 0.000001) == 0.5
    assert pytest.approx(res[1], 0.000001) == 0.5

def test_centroid_open_counterclockwise_2():
    res1 = polygon_centroid([[0, 0], [1, 0], [1, 1], [0, 1]])
    assert pytest.approx(res1[0], 0.000001) == 0.5
    assert pytest.approx(res1[1], 0.000001) == 0.5

    res2 = polygon_centroid([[1, 1], [3, 2], [2, 3]])
    assert pytest.approx(res2[0], 0.000001) == 2
    assert pytest.approx(res2[1], 0.000001) == 2

def test_centroid_very_large_polygon():
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
    res = polygon_centroid(points)
    assert pytest.approx(res[0], 0.00001) == 49999999.75000187
    assert pytest.approx(res[1], 0.00001) == 49999999.75001216