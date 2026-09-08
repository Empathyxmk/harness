import pytest
import numpy as np

from src.lips.intersectrayspolys import intersectrayspolys

def test_intersect_single_ray_different_polygon():
    rays = {'o': np.array([[5, 1, 1]]), 'd': np.array([[0, 0, 1]])}
    polygon = np.array([[2, 2, 7], [8, 2, 7], [8, 9, 7], [2, 9, 7]])
    polygons = [polygon]
    pts, idx = intersectrayspolys(rays, polygons)
    assert pts.shape == (1, 3)
    assert idx == 1 or idx == [1] or idx == [0]  # Depending on implementation (1-based vs 0-based)

def test_intersect_no_intersection_public():
    rays = {'o': np.array([[100, 100, 100]]), 'd': np.array([[0, 1, 0]])}
    polygon = np.array([[2, 2, 5], [8, 2, 5], [8, 9, 5], [2, 9, 5]])
    polygons = [polygon]
    pts, idx = intersectrayspolys(rays, polygons)
    assert pts is None or (hasattr(pts, '__len__') and len(pts) == 0)
    assert idx is None or (hasattr(idx, '__len__') and len(idx) == 0)