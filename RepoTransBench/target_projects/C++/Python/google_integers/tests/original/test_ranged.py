import pytest

def in_range(value, low, high):
    return (value >= low) and (value <= high)

def test_in_range():
    assert in_range(3, 1, 5)    # normal in
    assert not in_range(0, 1, 5)   # below
    assert not in_range(6, 1, 5)   # above
    assert in_range(1, 1, 5)    # boundary low
    assert in_range(5, 1, 5)    # boundary high

def test_negative_range():
    assert in_range(-2, -5, 0)    # inside negative range
    assert not in_range(-6, -5, 0)   # below negative