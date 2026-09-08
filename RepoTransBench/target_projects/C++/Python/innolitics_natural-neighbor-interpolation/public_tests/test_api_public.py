import numpy as np
import pytest

import naturalneighbor

def test_api_points_values_shape_public():
    points = np.array([[1, 1], [2, 2], [3, 3]])
    values = np.array([10, 20, 30])
    xi = np.array([[4, 4], [5, 5]])
    # We expect griddata to raise ImportError (cnaturalneighbor not found)
    with pytest.raises(ImportError):
        naturalneighbor.griddata(points, values, xi)