import numpy as np

import pytest

from src.unmix.soft import soft

def test_negative_scalar():
    x = -7
    T = 3
    expectedY = -4
    actualY = soft(x, T)
    assert np.isclose(actualY, expectedY, atol=1e-10)

def test_zero_threshold():
    x = 8
    T = 0
    expectedY = 8
    actualY = soft(x, T)
    assert np.isclose(actualY, expectedY, atol=1e-10)

def test_zero_input():
    x = 0
    T = 5
    expectedY = 0
    actualY = soft(x, T)
    assert np.isclose(actualY, expectedY, atol=1e-10)

def test_vector_input():
    x = np.array([-3, 0, 10])
    T = 4
    expectedY = np.array([0, 0, 6])
    actualY = soft(x, T)
    assert np.allclose(actualY, expectedY, atol=1e-10)

def test_negative_threshold():
    x = np.array([4, -5, 6])
    T = -2
    expectedY = np.array([4, -5, 6])
    actualY = soft(x, T)
    assert np.allclose(actualY, expectedY, atol=1e-10)