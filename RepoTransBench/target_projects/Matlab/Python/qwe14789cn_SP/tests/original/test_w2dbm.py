import pytest
from src.sp import w2dbm

def test_1mw():
    assert abs(w2dbm(1e-3) - 0) < 1e-10

def test_10mw():
    assert abs(w2dbm(1e-2) - 10) < 1e-10

def test_1w():
    assert abs(w2dbm(1) - 30) < 1e-8

def test_zero_w():
    with pytest.raises(Exception):
        w2dbm(0)