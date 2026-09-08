import numpy as np
from numpy.testing import assert_allclose

from naturalneighbor.naturalneighbor import _xyz_to_ijk

def test_identity_3x3_public():
    starts = np.array([1, 1, 1])
    steps = np.array([1, 1, 1])
    num_dimensions = 3
    num_points = 5
    points_xyz = np.random.uniform(5, 10, (num_points, num_dimensions))
    actual_points_ijk = _xyz_to_ijk(points_xyz, starts, steps)
    expected_points_ijk = points_xyz - 1
    assert_allclose(actual_points_ijk, expected_points_ijk, rtol=0, atol=1e-10)

def test_shift_3x3_public():
    starts = np.array([2, 3, -5])
    steps = np.array([1, 1, 1])
    points_xyz = np.array([[2, 3, -5], [4, 7, 0]])
    actual_points_ijk = _xyz_to_ijk(points_xyz, starts, steps)
    expected_points_ijk = np.array([[0, 0, 0], [2, 4, 5]])
    assert_allclose(actual_points_ijk, expected_points_ijk, rtol=0, atol=1e-10)

def test_shift_and_scale_3x3_public():
    starts = np.array([10, -2, 5])
    steps = np.array([2, 0.25, 0.5])
    points_xyz = np.array([[12, 0, 9], [14, 2, 7]])
    actual_points_ijk = _xyz_to_ijk(points_xyz, starts, steps)
    expected_points_ijk = np.array([
        [(12-10)/2, (0+2)/0.25, (9-5)/0.5],
        [(14-10)/2, (2+2)/0.25, (7-5)/0.5]
    ])
    assert_allclose(actual_points_ijk, expected_points_ijk, rtol=0, atol=1e-10)