import pytest
import numpy as np

from src.lips.gencirclerays import gencirclerays

def test_full_circle_rays():
    center = np.array([4, 5, 6])
    normal = np.array([0, 1, 0])
    n_rays = 10
    rays = gencirclerays(center, normal, n_rays)
    assert rays['o'].shape == (n_rays, 3)
    assert rays['d'].shape == (n_rays, 3)

def test_partial_arc_rays():
    center = np.array([-3, 2, 8])
    normal = np.array([1, 0, 0])
    n_rays = 7
    angle = np.pi / 2
    rays = gencirclerays(center, normal, n_rays, angle)
    assert rays['o'].shape == (n_rays, 3)

def test_different_radius():
    center = np.array([2, 4, 8])
    normal = np.array([0, 0, 1])
    n_rays = 9
    radius = 3.2
    rays = gencirclerays(center, normal, n_rays, 2 * np.pi, radius)
    assert rays['o'].shape == (n_rays, 3)

def test_fails_on_bad_normal_public():
    center = np.array([5, -5, 1])
    normal = np.array([0, 0, 0])
    n_rays = 4
    with pytest.raises(Exception):
        gencirclerays(center, normal, n_rays)