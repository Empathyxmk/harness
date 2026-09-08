import pytest
from potpourri3d import core

def test_dists_between_points_public():
    pts = [[2, 2, 2], [5, 6, 2], [2, 2, 5]]
    d0 = core.euclidean_distance(pts[0], pts[1])
    d1 = core.euclidean_distance(pts[0], pts[2])
    assert pytest.approx(d0) == 5.0
    assert pytest.approx(d1) == 3.0

def test_midpoint_public():
    ptA = [1, 3, 5]
    ptB = [5, 7, 9]
    mid = core.midpoint(ptA, ptB)
    assert mid == [3, 5, 7]

def test_cross_and_dot_public():
    a = [0, 2, 0]
    b = [0, 0, 3]
    c = core.cross(a, b)
    assert c == [6, 0, 0]
    d = core.dot(a, b)
    assert d == 0