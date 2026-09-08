from d3polygon import cross

def test_cross_counterclockwise():
    assert cross([0, 0], [1, 0], [0, 1]) > 0

def test_cross_clockwise():
    assert cross([0, 0], [0, 1], [1, 0]) < 0

def test_cross_collinear_points():
    assert cross([0, 0], [1, 1], [2, 2]) == 0

def test_cross_same_points():
    assert cross([1, 1], [1, 1], [1, 1]) == 0

def test_cross_negative_coordinates():
    assert cross([-1, 0], [0, -1], [1, 0]) == 2