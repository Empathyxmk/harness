import pytest
from src.sp import d2b

def test_int_positive():
    assert d2b(6, 4) == '0110'

def test_int_negative():
    out = d2b(-2, 3)
    assert len(out) == 3

def test_int_zero():
    assert d2b(0, 4) == '0000'

def test_larger_len():
    s = d2b(15, 8)
    assert len(s) == 8