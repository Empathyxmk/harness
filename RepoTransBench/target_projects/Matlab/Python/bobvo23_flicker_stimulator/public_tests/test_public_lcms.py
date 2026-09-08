import pytest
from src.lcms import lcms

def test_public_lcms_diff():
    assert lcms(7, 5) == 35

def test_public_lcms_zero():
    assert lcms(0, 17) == 0

def test_public_lcms_alternate():
    assert lcms(12, 4) == 12

def test_public_lcms_both_zero():
    assert lcms(0, 0) == 0

def test_public_lcms_empty_input():
    with pytest.raises(TypeError):
        lcms([], 10)