import pytest

def util_min(a, b):
    return min(a, b)
def util_max(a, b):
    return max(a, b)
def util_clamp(val, minv, maxv):
    return max(minv, min(maxv, val))

def test_util_min_max_clamp_public():
    assert util_min(7, 13) == 7
    assert util_min(-10, 10) == -10
    assert util_max(8, 3) == 8
    assert util_max(-8, -5) == -5
    assert util_clamp(3, 2, 6) == 3
    assert util_clamp(-7, 0, 5) == 0
    assert util_clamp(18, 1, 17) == 17