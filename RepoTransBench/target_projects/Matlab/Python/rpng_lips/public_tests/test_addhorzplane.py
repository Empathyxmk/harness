import pytest
import numpy as np

from src.lips.addhorzplane import addhorzplane

def test_alternative_add():
    floorPolys = [np.array([[1, 2], [3, 2], [3, 4], [1, 4]])]
    z = 5
    thickness = 1.1
    n_expected = 2
    output = addhorzplane(floorPolys, z, thickness)
    assert len(output) == n_expected

def test_empty_input_public():
    floorPolys = []
    z = -3.4
    thickness = 10
    output = addhorzplane(floorPolys, z, thickness)
    assert output == [] or (hasattr(output, '__len__') and len(output) == 0)

def test_zero_thickness_different_poly():
    floorPolys = [np.array([[5, 6], [7, 6], [7, 8], [5, 8]])]
    z = 53
    thickness = 0
    output = addhorzplane(floorPolys, z, thickness)
    assert len(output) == 2