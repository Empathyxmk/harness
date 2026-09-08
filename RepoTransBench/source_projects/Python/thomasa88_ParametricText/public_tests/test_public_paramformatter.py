import sys
import os
import pytest

# Ensure imports work when running as separate directory test
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from paramformatter import mixed_frac_inch

def make_param(val, unit=''):
    class Param:
        def __init__(self, v, u=''):
            self.value = v
            self.unit = u
        def __float__(self):
            return float(self.value)
        def __int__(self):
            return int(self.value)
        def __repr__(self):
            return f"Param({self.value!r},{self.unit!r})"
    return Param(val, unit)

def test_mixed_frac_inch_whole_number():
    p = make_param(15)
    assert mixed_frac_inch(p, None) == "15"

def test_mixed_frac_inch_simple_fraction():
    p = make_param(0.625)
    assert mixed_frac_inch(p, None) == "5/8"

def test_mixed_frac_inch_mixed():
    p = make_param(3.75)
    assert mixed_frac_inch(p, None) == "3 3/4"

def test_mixed_frac_inch_exact_half():
    p = make_param(6.5)
    assert mixed_frac_inch(p, None) == "6 1/2"

def test_mixed_frac_inch_zero():
    p = make_param(0)
    assert mixed_frac_inch(p, None) == "0"