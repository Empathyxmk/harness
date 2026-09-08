import pytest
from src.sp import vpp2dbm
import math

def test_vpp2():
    d = vpp2dbm(2, 50)
    assert not math.isnan(d)

def test_vpp7():
    d = vpp2dbm(7, 50)
    assert d > -10

def test_vpp_negative():
    with pytest.raises(Exception):
        vpp2dbm(-1, 50)

def test_impedance_variation():
    d1 = vpp2dbm(3, 25)
    d2 = vpp2dbm(3, 60)
    assert abs(d1 - d2) > 0