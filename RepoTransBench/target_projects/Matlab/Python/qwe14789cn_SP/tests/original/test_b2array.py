import pytest
from src.sp import b2array

def test_simple():
    arr = b2array('10101')
    assert all(arr == [1, 0, 1, 0, 1])

def test_char_array():
    arr = b2array(['1', '0', '1'])
    assert all(arr == [1, 0, 1])

def test_zeros_input():
    arr = b2array('00000')
    assert all(x == 0 for x in arr)

def test_ones_input():
    arr = b2array('11111')
    assert all(x == 1 for x in arr)