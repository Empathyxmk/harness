import pytest
import numpy as np
from src.sp import find_nearest_pos

def test_middle():
    LUT = np.array([-1, 0, 1, 2, 3])
    data = 1.6
    actual = find_nearest_pos(LUT, data)
    expected = np.argmin(np.abs(LUT - data))
    assert actual == expected

def test_exact_hit():
    LUT = np.array([10, 20, 30, 40, 50])
    data = 30
    actual = find_nearest_pos(LUT, data)
    assert actual == 2

def test_multiple_nearest():
    LUT = np.array([0, 5, 10, 15, 20])
    data = 12.5
    expected = np.argmin(np.abs(LUT - data))
    actual = find_nearest_pos(LUT, data)
    assert actual == expected

def test_single_element():
    LUT = np.array([7])
    data = 100
    actual = find_nearest_pos(LUT, data)
    assert actual == 0

def test_negative():
    LUT = np.array([-10, -5, 0, 5])
    data = -6
    actual = find_nearest_pos(LUT, data)
    assert actual == 1