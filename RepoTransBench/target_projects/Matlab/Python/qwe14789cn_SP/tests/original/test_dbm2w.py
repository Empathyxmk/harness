import pytest
from src.sp import dbm2w

def test_dbm_to_watt0():
    assert abs(dbm2w(0) - 1e-3) < 1e-12

def test_dbm_to_watt10():
    assert abs(dbm2w(10) - 1e-2) < 1e-12

def test_dbm_to_watt_minus10():
    assert abs(dbm2w(-10) - 1e-4) < 1e-12

def test_very_large():
    assert abs(dbm2w(100) - 1000) < 1e-2