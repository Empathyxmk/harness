import pytest
import math

# Dummy APFloat, replace with correct implementation as needed
class APFloat:
    def __init__(self, d):
        self.value = d

    def convert_to_double(self):
        return self.value

    def __eq__(self, other):
        return isinstance(other, APFloat) and self.value == other.value

def test_construct_and_convert_to_double():
    f1 = APFloat(3.14)
    assert math.isclose(f1.convert_to_double(), 3.14, rel_tol=0, abs_tol=1e-8)
    f2 = APFloat(-42.5)
    assert math.isclose(f2.convert_to_double(), -42.5, rel_tol=0, abs_tol=1e-8)

def test_apfloat_equality():
    f1 = APFloat(2.718)
    f2 = APFloat(2.718)
    f3 = APFloat(3.1415)
    assert f1 == f2
    assert not (f1 == f3)