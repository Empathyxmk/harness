import math
import pytest
from src.solvers.ffm.ffm import sigmoid

def min_val(a, b):
    return a if a < b else b

def max_val(a, b):
    return a if a > b else b

def test_sigmoid():
    """
    Test the sigmoid function with specific inputs.
    """
    r1 = sigmoid(2.0)
    assert abs(r1 - 0.8807971) < 1e-6, f"sigmoid(2.0) failed: got {r1}, expected 0.8807971"

    r2 = sigmoid(-3.0)
    assert abs(r2 - 0.04742587) < 1e-6, f"sigmoid(-3.0) failed: got {r2}, expected 0.04742587"

def test_min():
    """
    Test the minimum function with specific inputs.
    """
    assert min_val(5, 6) == 5, f"min(5,6) failed: got {min_val(5, 6)}, expected 5"
    assert min_val(-2, -1) == -2, f"min(-2,-1) failed: got {min_val(-2, -1)}, expected -2"

def test_max():
    """
    Test the maximum function with specific inputs.
    """
    assert max_val(5, 6) == 6, f"max(5,6) failed: got {max_val(5, 6)}, expected 6"
    assert max_val(-2, -1) == -1, f"max(-2,-1) failed: got {max_val(-2, -1)}, expected -1"