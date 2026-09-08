import numpy as np
import pytest

from src.unmix.soft import soft

def test_positive_scalar():
    x = 5
    T = 2
    expectedY = 3
    actualY = soft(x, T)
    assert np.isclose(actualY, expectedY, atol=1e-9)

def test_negative_scalar():
    x = -5
    T = 2
    expectedY = -3
    actualY = soft(x, T)
    assert np.isclose(actualY, expectedY, atol=1e-9)

def test_zero_x():
    x = 0
    T = 2
    expectedY = 0
    actualY = soft(x, T)
    assert np.isclose(actualY, expectedY, atol=1e-9)

def test_t_greater_than_abs_x():
    x = 2
    T = 5
    expectedY = 0
    actualY = soft(x, T)
    assert np.isclose(actualY, expectedY, atol=1e-9)

def test_t_equals_abs_x():
    x = 5
    T = 5
    expectedY = 0
    actualY = soft(x, T)
    assert np.isclose(actualY, expectedY, atol=1e-9)

def test_vector_input():
    x = np.array([-5, 0, 5, -3, 7])
    T = 2
    expectedY = np.array([-3, 0, 3, 0, 5])
    actualY = soft(x, T)
    assert np.allclose(actualY, expectedY, atol=1e-9)

def test_zero_t():
    x = np.array([5, 0, -5, 1e-10, -1e-10])
    T = 0
    expectedY = np.array([5, 0, -5, 0, 0]) # As in MATLAB logic and docstring
    actualY = soft(x, T)
    assert np.allclose(actualY, expectedY, atol=1e-9)

def test_large_t():
    x = 100
    T = 1e6
    expectedY = 0
    actualY = soft(x, T)
    assert np.isclose(actualY, expectedY, atol=1e-9)

def test_matrix_input():
    x = np.array([[1,2],[3,-4]])
    T = 1.5
    expectedY = np.array([[0,0.5],[1.5,-2.5]])
    actualY = soft(x, T)
    assert np.allclose(actualY, expectedY, atol=1e-9)