import pytest
import numpy as np
import naturalneighbor

def test_cube_griddata_importerror():
    points = np.random.rand(8, 3)
    values = np.random.rand(8)
    xi = np.random.rand(3)
    try:
        naturalneighbor.griddata(points, values, xi)
    except ImportError as e:
        assert "cnaturalneighbor" in str(e)

def test_cube_xyz_to_ijk_array():
    import naturalneighbor.naturalneighbor as nn
    xyz = np.array([[0., 0., 0.], [1., 2., 3.], [2., 4., 1.]])
    origin = [0., 0., 0.]
    spacing = [1., 2., 1.]
    expected = np.array([
        [0., 0., 0.],
        [1., 1., 3.],
        [2., 2., 1.]
    ])
    np.testing.assert_allclose(nn._xyz_to_ijk(xyz, origin, spacing), expected)