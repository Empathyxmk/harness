import pytest
from src.sp import w2dbm

def test_1mwatt():
    dbm = w2dbm(1e-3)
    assert abs(dbm - 0) < 1e-8

def test_10mwatt():
    dbm = w2dbm(10e-3)
    assert abs(dbm - 10) < 1e-8

def test_0_1mwatt():
    dbm = w2dbm(0.1e-3)
    assert abs(dbm + 10) < 1e-8