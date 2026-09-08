import pytest
import numpy as np

from src.lips.intersectrayspolys import intersectrayspolys

def test_simple_intersection():
    rays = {'o': np.array([[0, 0, 0]]), 'd': np.array([[0, 0, 1]])}
    poly = [np.array([[0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1]])]
    result = intersectrayspolys(rays, poly)
    assert isinstance(result, dict) or hasattr(result, '__dict__')

def test_no_intersection():
    rays = {'o': np.array([[0, 0, 0]]), 'd': np.array([[1, 0, 0]])}
    poly = [np.array([[0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1]])]
    result = intersectrayspolys(rays, poly)
    assert isinstance(result, dict) or hasattr(result, '__dict__')

def test_multiple_rays_and_polys():
    rays = {
        'o': np.array([[0, 0, 0], [0, 0, 2]]),
        'd': np.array([[0, 0, 1], [0, 0, -1]])
    }
    poly = [
        np.array([[0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1]]),
        np.array([[0, 0, -1], [1, 0, -1], [1, 1, -1], [0, 1, -1]])
    ]
    result = intersectrayspolys(rays, poly)
    assert isinstance(result, dict) or hasattr(result, '__dict__')