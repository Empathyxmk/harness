import pytest

def in_range(value, low, high):
    return (value >= low) and (value <= high)

def test_in_range_public():
    assert in_range(10, 7, 15)   # normal in
    assert not in_range(6, 7, 15)   # below
    assert not in_range(16, 7, 15)  # above
    assert in_range(7, 7, 15)    # boundary low
    assert in_range(15, 7, 15)   # boundary high

def test_negative_range_public():
    assert in_range(-3, -5, -2)      # inside negative range
    assert not in_range(-6, -5, -2)  # below negative
    assert in_range(-2, -5, -2)      # boundary
    assert not in_range(0, -5, -2)   # above all negative range