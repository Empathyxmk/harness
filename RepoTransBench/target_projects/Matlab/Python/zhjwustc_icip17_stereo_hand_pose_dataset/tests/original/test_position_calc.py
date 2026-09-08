import numpy as np
import pytest

from src.handpose.position_calc import position_calc
from src.handpose.rodrigues import rodrigues

def test_basic_calculation():
    depthIm = np.ones((500, 500)) * 1000
    depthPosition = [250, 250]
    depthIJK, depthXYZ, colorIJK, colorXYZ = position_calc(depthPosition, depth_im=depthIm)
    assert depthIJK.shape == (3, 1)
    assert depthXYZ.shape == (3, 1)
    assert colorIJK.shape == (3, 1)
    assert colorXYZ.shape == (3, 1)
    # Not NaN or Inf
    for arr in [depthIJK, depthXYZ, colorIJK, colorXYZ]:
        assert not np.any(np.isnan(arr))
        assert not np.any(np.isinf(arr))
    assert abs(colorIJK[2,0] - 1) < 1e-9
    # Not all zeros
    for arr in [depthIJK, depthXYZ, colorIJK, colorXYZ]:
        assert not np.all(arr == 0)

def test_out_of_bounds_depth_position():
    depthIm = np.ones((10, 10)) * 500
    depthPositionOutOfBounds = [100, 100]
    with pytest.raises(IndexError):
        position_calc(depthPositionOutOfBounds, depth_im=depthIm)

def test_zero_depth_value_at_position():
    depthIm = np.ones((500, 500))
    depthIm[249, 249] = 0 # 0-based indexing
    depthPosition = [250, 250]
    _, depthXYZ, _, _ = position_calc(depthPosition, depth_im=depthIm)
    assert np.allclose(depthXYZ, np.zeros((3,1)))

def test_depth_position_on_boundary():
    depthIm = np.ones((100, 100)) * 1000
    positions = [
        [1, 1],
        [100, 100],
        [1, 50],
        [50, 1]
    ]
    for pos in positions:
        position_calc(pos, depth_im=depthIm)
    assert True  # No error means pass

def test_rodrigues_small_angle():
    r_small = [1e-10, 2e-10, 3e-10]
    R = rodrigues(r_small)
    assert np.allclose(R, np.eye(3), atol=1e-8)