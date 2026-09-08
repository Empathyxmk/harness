import numpy as np
from src.pde_utils.sigmoid import sigmoid

def test_sigmoid_positive():
    x_pos = 1.0
    expected_pos = 1.0 / (1.0 + np.exp(-x_pos))
    actual_pos = sigmoid(x_pos)
    assert abs(actual_pos - expected_pos) < 1e-9

def test_sigmoid_negative():
    x_neg = -1.0
    expected_neg = 1.0 / (1.0 + np.exp(-x_neg))
    actual_neg = sigmoid(x_neg)
    assert abs(actual_neg - expected_neg) < 1e-9

def test_sigmoid_zero():
    x_zero = 0.0
    expected_zero = 0.5
    actual_zero = sigmoid(x_zero)
    assert abs(actual_zero - expected_zero) < 1e-9

def test_sigmoid_large_positive():
    x_large_pos = 100.0
    actual_large_pos = sigmoid(x_large_pos)
    assert actual_large_pos > 0.999999999

def test_sigmoid_large_negative():
    x_large_neg = -100.0
    actual_large_neg = sigmoid(x_large_neg)
    assert actual_large_neg < 0.000000001