import math
import pytest
from src.solvers.ffm.ffm import sigmoid

def test_sigmoid_distinct():
    """
    Test the sigmoid function with different inputs than the original tests.
    """
    x = -2.0
    y = 0.0
    z = 2.0
    a = 8.0

    sx = sigmoid(x)
    sy = sigmoid(y)
    sz = sigmoid(z)
    sa = sigmoid(a)

    assert abs(sx - 0.11920292) < 1e-6, f"sigmoid(-2.0) failed: got {sx}, expected 0.11920292"
    assert abs(sy - 0.5) < 1e-7, f"sigmoid(0.0) failed: got {sy}, expected 0.5"
    assert abs(sz - 0.88079707) < 1e-6, f"sigmoid(2.0) failed: got {sz}, expected 0.88079707"
    assert abs(sa - 0.9996646) < 1e-6, f"sigmoid(8.0) failed: got {sa}, expected 0.9996646"