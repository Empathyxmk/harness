import pytest
from src.sp import h2f

def test_no_sign():
    f = h2f('1C', 2, 2, False)
    assert abs(f-7) < 1

def test_sign():
    f = h2f('FF', 2, 2, True)
    assert f < 0