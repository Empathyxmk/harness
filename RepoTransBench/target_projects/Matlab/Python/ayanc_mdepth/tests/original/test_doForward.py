import pytest
import numpy as np

from src.ayanc_mdepth.doForward import doForward

def test_simple_forward():
    # Example: using a random input array
    X = np.array([1, 2, 3])
    W = np.array([[4], [5], [6]])
    B = 7
    # Matlab: Y = W' * X' + B;
    Y_expected = np.dot(W.T, X) + B
    Y_actual = doForward(X, W, B)
    assert np.allclose(Y_actual, Y_expected), f"Expected {Y_expected}, but got {Y_actual}"