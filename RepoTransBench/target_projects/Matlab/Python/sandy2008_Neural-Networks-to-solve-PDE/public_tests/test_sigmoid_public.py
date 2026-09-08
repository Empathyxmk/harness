import numpy as np
from src.pde_utils.sigmoid import sigmoid

def test_sigmoid_public_0():
    assert abs(sigmoid(0) - 0.5) < 1e-6

def test_sigmoid_public_1():
    assert abs(sigmoid(1) - (1 / (1 + np.exp(-1)))) < 1e-6

def test_sigmoid_public_minus3():
    assert abs(sigmoid(-3) - (1 / (1 + np.exp(3)))) < 1e-6

def test_sigmoid_public_2_5():
    assert abs(sigmoid(2.5) - (1 / (1 + np.exp(-2.5)))) < 1e-6