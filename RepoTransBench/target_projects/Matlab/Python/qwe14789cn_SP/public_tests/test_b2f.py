import pytest
from src.sp import b2f

def test_simple():
    f = b2f('0011', 4, 2)
    assert abs(f - 0.75) < 1e-6

def test_sign():
    f = b2f('1111', 4, 2, True)
    assert f < 0

def test_all_ones():
    f = b2f('1111', 4, 3, False)
    assert abs(f - 1.875) < 1e-6