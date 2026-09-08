import pytest
from src.sp import d2h

def test_unsigned():
    hexstr = d2h(255, 8, False)
    assert hexstr == '000000ff' or hexstr == 'FF'

def test_signed():
    hexstr = d2h(-1, 2, True)
    valid = ['ff','FF','FFFF','ffffffff']
    assert any(hexstr.lower() == v.lower() for v in valid)

def test_zero():
    hexstr = d2h(0, 4, False)
    assert hexstr.lower() == '0000' or hexstr.lower() == '00000000'

def test_negative():
    with pytest.raises(Exception):
        d2h(-999, 4, False)