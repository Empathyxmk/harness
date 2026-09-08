import pytest
import numpy as np

from src.lips.euler2angular import euler2angular

def test_zero_angles():
    alpha, beta, gamma = 0, 0, 0
    x = euler2angular(np.array([alpha, beta, gamma]))
    np.testing.assert_allclose(x, [0, 0, 0], atol=1e-9)

def test_pi_angles():
    alpha = np.pi
    beta = np.pi / 2
    gamma = np.pi / 3
    y = euler2angular(np.array([alpha, beta, gamma]))
    assert y.shape == (3,) or y.shape == (1, 3)

def test_error_input():
    with pytest.raises(Exception):
        euler2angular(np.array([1, 2]))