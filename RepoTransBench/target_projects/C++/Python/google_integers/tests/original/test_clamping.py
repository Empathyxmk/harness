import pytest

def clamp(x, low, high):
    return low if x < low else (high if x > high else x)

def test_clamp_values():
    low = 2
    high = 5
    x1 = 1
    x2 = 7
    x3 = 4

    assert clamp(x1, low, high) == 2  # x1 was below range
    assert clamp(x2, low, high) == 5  # x2 was above range
    assert clamp(x3, low, high) == 4  # x3 was in the range

def test_clamp_edge_cases():
    low = 0
    high = 10

    # exactly at bounds
    assert clamp(0, low, high) == 0
    assert clamp(10, low, high) == 10

    # negative infinity
    assert clamp(-1000, low, high) == 0

    # positive infinity
    assert clamp(1000, low, high) == 10