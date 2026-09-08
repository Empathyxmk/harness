import pytest
from src.sp import dbm2vpp

def test_zero_dbm():
    out = dbm2vpp(0, 50)
    assert out > 0

def test_10_dbm():
    out = dbm2vpp(10, 50)
    assert out > 0

def test_negative_dbm():
    out = dbm2vpp(-10, 75)
    assert out > 0

def test_large_dbm():
    out = dbm2vpp(40, 50)
    assert out > 0