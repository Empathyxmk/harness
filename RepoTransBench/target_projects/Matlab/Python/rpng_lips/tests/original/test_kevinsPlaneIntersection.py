import pytest
import numpy as np

from src.lips.kevinsPlaneIntersection import kevinsPlaneIntersection

def test_xy_plane():
    p1 = np.array([0, 0, 0])
    n1 = np.array([0, 0, 1])
    p2 = np.array([1, 0, 0])
    n2 = np.array([0, 1, 0])
    p, d = kevinsPlaneIntersection(p1, n1, p2, n2)
    assert p.shape == (3,)
    assert d.shape == (3,)

def test_parallel_planes():
    p1 = np.array([0, 0, 0])
    n1 = np.array([0, 0, 1])
    p2 = np.array([0, 0, 1])
    n2 = np.array([0, 0, 1])
    p, d = kevinsPlaneIntersection(p1, n1, p2, n2)
    assert np.all(np.isnan(p)) and np.all(np.isnan(d))