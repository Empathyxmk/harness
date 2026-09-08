import pytest
from potpourri3d import core

def test_dists_between_points():
    pts = [[0, 0, 0], [1, 0, 0], [1, 1, 0]]
    d0 = core.euclidean_distance(pts[0], pts[1])
    d1 = core.euclidean_distance(pts[1], pts[2])
    assert pytest.approx(d0) == 1.0
    assert pytest.approx(d1) == 1.0

def test_midpoint():
    ptA = [0, 0, 0]
    ptB = [2, 2, 2]
    mid = core.midpoint(ptA, ptB)
    assert mid == [1, 1, 1]

def test_cross_and_dot():
    a = [1, 0, 0]
    b = [0, 1, 0]
    c = core.cross(a, b)
    assert c == [0, 0, 1]
    d = core.dot(a, b)
    assert d == 0