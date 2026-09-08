import pytest
from src.sp import d2h

def test_ten():
    s = d2h(10, 4, False)
    assert s.lower() == 'a'

def test_other_number():
    s = d2h(20, 6, False)
    assert s.lower() == '14'

def test_zero():
    s = d2h(0, 2, False)
    assert s.lower() == '0'