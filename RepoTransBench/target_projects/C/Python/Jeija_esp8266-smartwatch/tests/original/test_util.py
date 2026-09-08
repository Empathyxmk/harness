import pytest

# Mock util API
def util_min(a, b):
    return min(a, b)
def util_max(a, b):
    return max(a, b)
def util_clamp(val, minv, maxv):
    return max(minv, min(maxv, val))

def test_util_min_max_clamp():
    assert util_min(2, 3) == 2
    assert util_min(10, -3) == -3
    assert util_max(2, 3) == 3
    assert util_max(10, -3) == 10
    assert util_clamp(1, 0, 2) == 1
    assert util_clamp(-1, 0, 2) == 0
    assert util_clamp(5, 0, 2) == 2