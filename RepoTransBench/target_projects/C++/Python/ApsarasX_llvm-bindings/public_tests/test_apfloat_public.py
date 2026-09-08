import pytest
import math

# Dummy APFloat for public test
class APFloat:
    def __init__(self, d):
        self.value = d

    def convert_to_double(self):
        return self.value

    def __eq__(self, other):
        return isinstance(other, APFloat) and self.value == other.value

def test_construct_and_convert_to_double_public():
    f1 = APFloat(1.23)
    assert math.isclose(f1.convert_to_double(), 1.23, rel_tol=0, abs_tol=1e-8)
    f2 = APFloat(-67.89)
    assert math.isclose(f2.convert_to_double(), -67.89, rel_tol=0, abs_tol=1e-8)

def test_apfloat_equality_public():
    f1 = APFloat(7.77)
    f2 = APFloat(7.77)
    f3 = APFloat(0.12345)
    assert f1 == f2
    assert not (f1 == f3)