import pytest
import numpy as np

from src.lips.gencirclerays import gencirclerays

def test_circle_arc_360():
    center = np.array([0, 0, 0])
    normal = np.array([0, 0, 1])
    n_rays = 8
    rays = gencirclerays(center, normal, n_rays)
    assert rays['o'].shape == (n_rays, 3)
    assert rays['d'].shape == (n_rays, 3)

def test_circle_arc_partial():
    center = np.array([2, -2, 1])
    normal = np.array([0, 1, 0])
    n_rays = 5
    angle = np.pi
    rays = gencirclerays(center, normal, n_rays, angle)
    assert rays['o'].shape == (n_rays, 3)

def test_with_radius():
    center = np.array([1, 1, 1])
    normal = np.array([1, 0, 0])
    n_rays = 6
    radius = 4
    rays = gencirclerays(center, normal, n_rays, 2 * np.pi, radius)
    assert rays['o'].shape == (n_rays, 3)

def test_bad_normal():
    center = np.array([0, 0, 0])
    normal = np.array([0, 0, 0])
    n_rays = 3
    with pytest.raises(Exception):
        gencirclerays(center, normal, n_rays)