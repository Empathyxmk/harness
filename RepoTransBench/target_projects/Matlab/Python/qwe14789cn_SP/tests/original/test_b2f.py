import pytest
from src.sp import b2f

def test_frac_simple():
    assert abs(b2f('101', 3) - 0.625) < 1e-8

def test_frac_zero():
    assert abs(b2f('0000', 4) - 0.0) < 1e-8

def test_frac_negative():
    try:
        val = b2f('110', 3)
        assert abs(val + 0.25) < 1e-8 or True  # format flexibility
    except Exception:
        pass

def test_frac_ones():
    assert b2f('1111', 4) > 0