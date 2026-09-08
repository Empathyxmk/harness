import pytest
from src.sp import h2d

def test_positive():
    val = h2d('7A', 8, False)
    assert val == 122

def test_zero():
    val = h2d('0000', 16, False)
    assert val == 0

def test_negative():
    val = h2d('80', 8, True)
    assert val == -128