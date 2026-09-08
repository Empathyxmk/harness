import numpy as np
from src.shift import shift

def test_right_shift():
    x = [5, 6, 7, 8, 9, 10]
    y = shift(x, 3)
    assert np.array_equal(y, [8, 9, 10, 5, 6, 7])

def test_left_shift():
    x = [10, 20, 30, 40]
    y = shift(x, -1)
    assert np.array_equal(y, [20, 30, 40, 10])

def test_no_shift():
    x = [7, 8, 9]
    y = shift(x, 0)
    assert np.array_equal(y, x)

def test_shift_greater_than_length():
    x = [3, 1, 4, 1]
    y = shift(x, 6)  # same as shift(x,2)
    expected = shift(x,2)
    assert np.array_equal(y, expected)

def test_negative_shift_greater_than_length():
    x = [2, 4, 6, 8, 10]
    y = shift(x, -7)  # same as shift(x,-2)
    expected = shift(x,-2)
    assert np.array_equal(y, expected)