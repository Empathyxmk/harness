import numpy as np
import pytest
from multipolyregress import MultiPolyRegress

def test_simple_linear():
    # Test 1: Simple linear fit
    X = np.array([1, 2, 3, 4, 5])
    Y = 2 * X + 1
    degree = 1
    mpr = MultiPolyRegress(X, Y, degree)
    Y_pred = mpr.predict(X)
    assert np.allclose(Y, Y_pred, atol=1e-10)

def test_quadratic():
    # Test 2: Quadratic fit
    X = np.arange(1, 6)
    Y = 1 + 2 * X + 3 * X**2
    degree = 2
    mpr2 = MultiPolyRegress(X, Y, degree)
    Y_pred2 = mpr2.predict(X)
    assert np.allclose(Y, Y_pred2, atol=1e-10)

def test_multivariate_input():
    # Test 3: Multivariate input
    X = np.array([[1, 2],
                  [2, 3],
                  [3, 4],
                  [4, 5]])
    Y = 1 + X[:, 0] + X[:, 1]
    degree = 1
    mpr3 = MultiPolyRegress(X, Y, degree)
    Y_pred3 = mpr3.predict(X)
    assert np.allclose(Y, Y_pred3, atol=1e-10)