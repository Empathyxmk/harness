import pytest
from src.sp import vpp2dbm
import math

def test_vpp1():
    d = vpp2dbm(1, 50)
    assert not math.isnan(d)

def test_vpp10():
    d = vpp2dbm(10, 50)
    assert d > -10

def test_vpp_zero():
    with pytest.raises(Exception):
        vpp2dbm(0, 50)

def test_impedance_variation():
    d1 = vpp2dbm(5, 75)
    d2 = vpp2dbm(5, 100)
    assert abs(d1 - d2) > 0