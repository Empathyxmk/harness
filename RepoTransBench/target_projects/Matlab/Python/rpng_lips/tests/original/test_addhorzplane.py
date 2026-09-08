import pytest
import numpy as np

from src.lips.addhorzplane import addhorzplane

def test_basic_add():
    floorPolys = [np.array([[0, 0], [1, 0], [1, 1], [0, 1]])]
    z = 0
    thickness = 0.5
    n_expected = 2
    output = addhorzplane(floorPolys, z, thickness)
    assert len(output) == n_expected

def test_empty_input():
    floorPolys = []
    z = 2
    thickness = 1
    output = addhorzplane(floorPolys, z, thickness)
    assert output == [] or (hasattr(output, '__len__') and len(output) == 0)

def test_zero_thickness():
    floorPolys = [np.array([[0, 0], [2, 0], [2, 2], [0, 2]])]
    z = -1
    thickness = 0
    output = addhorzplane(floorPolys, z, thickness)
    assert len(output) == 2