import pytest
from src.sp import dbm2w

def test_0dbm():
    val = dbm2w(0)
    assert abs(val - 1e-3) < 1e-6

def test_minus5dbm():
    val = dbm2w(-5)
    assert val < 1e-3 and val > 0

def test_25dbm():
    val = dbm2w(25)
    assert val > 0.1