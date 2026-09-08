import numpy as np
from src.shift import shift

def test_right_shift():
    x = [1, 2, 3, 4, 5]
    y = shift(x, 2)
    assert np.array_equal(y, [4, 5, 1, 2, 3])

def test_left_shift():
    x = [1, 2, 3, 4, 5]
    y = shift(x, -2)
    assert np.array_equal(y, [3, 4, 5, 1, 2])

def test_no_shift():
    x = [1, 2, 3]
    y = shift(x, 0)
    assert np.array_equal(y, x)

def test_shift_greater_than_length():
    x = [1, 2, 3]
    y = shift(x, 4)  # same as shift(x,1)
    expected = shift(x, 1)
    assert np.array_equal(y, expected)

def test_negative_shift_greater_than_length():
    x = [1, 2, 3]
    y = shift(x, -4)  # same as shift(x,-1)
    expected = shift(x, -1)
    assert np.array_equal(y, expected)