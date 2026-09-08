import pytest
from src.sp import h2d

def test_positive():
    val = h2d('FF', 8, False)
    assert val == 255

def test_zero():
    val = h2d('00', 4, False)
    assert val == 0

def test_negative():
    val = h2d('FF', 8, True)
    assert val == -1