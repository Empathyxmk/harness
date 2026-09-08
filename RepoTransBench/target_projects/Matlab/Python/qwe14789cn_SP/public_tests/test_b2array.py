import pytest
from src.sp import b2array

def test_simple4bits():
    arr = b2array('1101', 4, False)
    assert list(arr) == [1,1,0,1]

def test_with_sign():
    arr = b2array('10100', 5, True)
    assert list(arr) == [1,0,1,0,0]