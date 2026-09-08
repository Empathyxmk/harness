import pytest

def clamp(x, low, high):
    return low if x < low else (high if x > high else x)

def test_clamp_values_public():
    low = -3
    high = 7
    x1 = -10
    x2 = 15
    x3 = 6

    assert clamp(x1, low, high) == -3  # x1 below range
    assert clamp(x2, low, high) == 7   # x2 above range
    assert clamp(x3, low, high) == 6   # x3 in range

def test_clamp_edge_cases_public():
    low = -5
    high = 5
    # at bounds
    assert clamp(-5, low, high) == -5
    assert clamp(5, low, high) == 5
    # way above/below
    assert clamp(100, low, high) == 5
    assert clamp(-100, low, high) == -5