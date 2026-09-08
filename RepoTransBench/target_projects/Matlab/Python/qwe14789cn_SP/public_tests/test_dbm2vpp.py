import pytest
from src.sp import dbm2vpp

def test_neg20_dbm():
    out = dbm2vpp(-20, 50)
    assert out > 0

def test_5_dbm():
    out = dbm2vpp(5, 75)
    assert out > 0

def test_20_dbm():
    out = dbm2vpp(20, 100)
    assert out > 0

def test_large_negative_dbm():
    out = dbm2vpp(-40, 50)
    assert out > 0