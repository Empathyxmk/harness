import pytest
from src.lcms import lcms

def test_lcms_basic():
    assert lcms(6, 8) == 24

def test_lcms_zero_first():
    assert lcms(0, 10) == 0

def test_lcms_nontrivial():
    assert lcms(9, 3) == 9

def test_lcms_both_zero():
    assert lcms(0, 0) == 0

def test_lcms_bad_type():
    with pytest.raises(TypeError):
        lcms('x', 10)