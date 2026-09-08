import pytest
import numpy as np

from src.ayanc_mdepth.doForward import doForward

def test_simple_forward():
    X = np.array([8, 3, 1])
    W = np.array([[2], [9], [5]])
    B = 4
    Y_expected = np.dot(W.T, X) + B
    Y_actual = doForward(X, W, B)
    assert np.allclose(Y_actual, Y_expected), f"Expected {Y_expected}, got {Y_actual}"