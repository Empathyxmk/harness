import pytest
import numpy as np

from src.lips.euler2angular import euler2angular

def test_euler_conversion_different_values():
    eul = np.array([0.8, -0.5, 1.2])
    v = euler2angular(eul)
    assert len(v) == 3

def test_euler_zeros():
    eul = np.array([0, 0, 0])
    v = euler2angular(eul)
    np.testing.assert_array_equal(v, [0, 0, 0])