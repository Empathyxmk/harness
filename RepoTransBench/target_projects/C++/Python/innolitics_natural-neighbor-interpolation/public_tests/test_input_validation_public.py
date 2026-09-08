import numpy as np
import pytest

import naturalneighbor

def test_wrong_shape_points_public():
    points = np.array([10, 20, 30, 40])
    values = np.array([1, 2, 3, 4])
    xi = np.array([[7, 8], [9, 10]])
    with pytest.raises(Exception):
        naturalneighbor.griddata(points, values, xi)

def test_wrong_shape_values_public():
    points = np.array([[1, 2], [3, 4], [5, 6]])
    values = np.array([1, 2, 3, 4])
    xi = np.array([[1, 2]])
    with pytest.raises(Exception):
        naturalneighbor.griddata(points, values, xi)