import pytest
from src.sp import b2d

def test_binary_positive():
    val = b2d('10101', 6)
    assert val == 21

def test_binary_zero():
    val = b2d('0', 3)
    assert val == 0

def test_binary_negative():
    val = b2d('111001', 6)
    assert val == -7