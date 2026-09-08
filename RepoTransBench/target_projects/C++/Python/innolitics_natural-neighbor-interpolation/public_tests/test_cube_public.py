import pytest

import numpy as np
import naturalneighbor

def test_cube_griddata_importerror_public():
    points = np.random.uniform(-1, 1, (8, 3))
    values = np.random.uniform(-10, 10, 8)
    xi = np.random.uniform(-1, 1, 3)
    try:
        naturalneighbor.griddata(points, values, xi)
    except ImportError as e:
        assert "cnaturalneighbor" in str(e)

def test_cube_xyz_to_ijk_array_public():
    import naturalneighbor.naturalneighbor as nn
    xyz = np.array([[3., 6., 9.], [5., 8., 2.], [7., 4., 11.]])
    origin = [3., 6., 2.]
    spacing = [1., 2., 3.]
    expected = np.array([
        [0., 0., 2.33333333],
        [2., 1., 0.],
        [4., -1., 3.]
    ])
    np.testing.assert_allclose(nn._xyz_to_ijk(xyz, origin, spacing), expected)