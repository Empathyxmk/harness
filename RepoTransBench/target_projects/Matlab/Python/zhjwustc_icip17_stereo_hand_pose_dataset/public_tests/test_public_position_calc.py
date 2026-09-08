import numpy as np
import pytest

from src.handpose.position_calc import position_calc

def test_basic_calculation_different_input():
    depthIm = np.ones((300, 300)) * 750
    depthPosition = [150, 100]
    depthIJK, depthXYZ, colorIJK, colorXYZ = position_calc(depthPosition, depth_im=depthIm)
    assert depthIJK.shape == (3, 1)
    assert depthXYZ.shape == (3, 1)
    assert colorIJK.shape == (3, 1)
    assert colorXYZ.shape == (3, 1)
    for arr in [depthIJK, depthXYZ, colorIJK, colorXYZ]:
        assert not np.any(np.isnan(arr))
        assert not np.any(np.isinf(arr))
    assert abs(colorIJK[2,0] - 1) < 1e-9
    for arr in [depthIJK, depthXYZ, colorIJK, colorXYZ]:
        assert not np.all(arr == 0)

def test_edge_case_out_of_bounds_depth_position_different():
    depthIm = np.ones((5, 12)) * 222
    depthPositionOutOfBounds = [99, 1]
    with pytest.raises(IndexError):
        position_calc(depthPositionOutOfBounds, depth_im=depthIm)

def test_edge_case_zero_depth_value_at_different_position():
    depthIm = np.ones((111, 111))
    depthIm[0, 10] = 0
    depthPosition = [11, 1]  # 1-based
    _, depthXYZ, _, _ = position_calc(depthPosition, depth_im=depthIm)
    assert np.allclose(depthXYZ, np.zeros((3,1)))

def test_edge_case_depth_position_on_boundary_different():
    depthIm = np.ones((42, 42)) * 123
    depthPosition = [42, 42]
    depthIJK, depthXYZ, colorIJK, colorXYZ = position_calc(depthPosition, depth_im=depthIm)
    assert depthIJK.shape == (3, 1)
    assert depthXYZ.shape == (3, 1)
    assert colorIJK.shape == (3, 1)
    assert colorXYZ.shape == (3, 1)
    assert abs(colorIJK[2,0] - 1) < 1e-9
    assert not np.any(np.isnan(depthIJK))
    assert not np.any(np.isinf(depthIJK))