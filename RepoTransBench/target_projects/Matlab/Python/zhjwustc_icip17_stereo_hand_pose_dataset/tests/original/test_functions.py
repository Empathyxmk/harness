import numpy as np
import pytest

from src.handpose.rodrigues import rodrigues, rodrigues_with_angle
from src.handpose.position_calc import position_calc

def test_rodrigues_x_axis_90_deg():
    """Test rodrigues: rotate around X-axis by 90 deg (pi/2)"""
    R_expected = np.array([
        [1, 0, 0],
        [0, np.cos(np.pi/2), -np.sin(np.pi/2)],
        [0, np.sin(np.pi/2), np.cos(np.pi/2)]
    ])
    r = [np.pi/2, 0, 0]
    R_actual = rodrigues(r)
    assert np.allclose(R_actual, R_expected, atol=1e-9)

def test_rodrigues_zero_rotation():
    R_expected = np.eye(3)
    r = [0, 0, 0]
    R_actual = rodrigues(r)
    assert np.allclose(R_actual, R_expected, atol=1e-9)

def test_rodrigues_z_axis_pi():
    R_expected = np.array([
        [-1, 0, 0],
        [0, -1, 0],
        [0, 0, 1]
    ])
    r = [0, 0, np.pi]
    R_actual = rodrigues(r)
    assert np.allclose(R_actual, R_expected, atol=1e-9)

def test_position_calc_single_keypoint_principal_point():
    fx = 500
    fy = 500
    cx = 320
    cy = 240
    K = np.array([[fx, 0, cx], [0, fy, cy], [0, 0, 1]])
    T_vec = np.array([0, 0, 1000])
    R_rod = [0, 0, 0]
    from src.handpose.rodrigues import rodrigues
    R_mat = rodrigues(R_rod)
    kp = [cx, cy]
    pos3D = position_calc(kp, K, R_mat, T_vec)
    assert pos3D.shape == (1, 3)
    assert not np.any(np.isnan(pos3D))

def test_position_calc_multiple_keypoints():
    fx = 500
    fy = 500
    cx = 320
    cy = 240
    K = np.array([[fx, 0, cx], [0, fy, cy], [0, 0, 1]])
    T_vec = np.array([0, 0, 1000])
    R_rod = [0, 0, 0]
    from src.handpose.rodrigues import rodrigues
    R_mat = rodrigues(R_rod)
    keypoints2D_2 = np.array([
        [cx, cy],
        [cx + 10, cy + 20],
        [cx - 5, cy + 15]
    ])
    pos3D = position_calc(keypoints2D_2, K, R_mat, T_vec)
    assert pos3D.shape == (3, 3)
    assert not np.any(np.isnan(pos3D))

def test_position_calc_empty_keypoints():
    fx = 500
    fy = 500
    cx = 320
    cy = 240
    K = np.array([[fx, 0, cx], [0, fy, cy], [0, 0, 1]])
    T_vec = np.array([0, 0, 1000])
    R_rod = [0, 0, 0]
    from src.handpose.rodrigues import rodrigues
    R_mat = rodrigues(R_rod)
    keypoints2D_empty = np.zeros((0, 2))
    pos3D_empty = position_calc(keypoints2D_empty, K, R_mat, T_vec)
    assert pos3D_empty.shape == (0, 3)