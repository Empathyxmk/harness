import pytest
import numpy as np

from src.lips.planes2dtopolygons3d import planes2dtopolygons3d

def test_typical_input():
    planes2d = [np.array([[0, 0], [1, 0], [1, 1], [0, 1]])]
    z = 2
    polys3d = planes2dtopolygons3d(planes2d, z)
    assert polys3d[0].shape[1] == 3
    assert np.all(polys3d[0][:, 2] == z)

def test_multiple_planes():
    planes2d = [
        np.array([[0, 0], [1, 0], [1, 1], [0, 1]]),
        np.array([[0.5, 0.5], [1.5, 0.5], [1.5, 1.5], [0.5, 1.5]])
    ]
    z = -1
    polys3d = planes2dtopolygons3d(planes2d, z)
    assert len(polys3d) == 2

def test_empty_input():
    polys3d = planes2dtopolygons3d([], 0)
    assert polys3d == [] or (hasattr(polys3d, '__len__') and len(polys3d) == 0)

def test_input_type_robustness():
    polys3d = planes2dtopolygons3d([np.array([[1, 2]])], 6.6)
    assert isinstance(polys3d[0], np.ndarray)