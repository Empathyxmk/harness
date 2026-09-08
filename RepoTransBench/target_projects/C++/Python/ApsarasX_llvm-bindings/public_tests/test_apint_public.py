import pytest

# Dummy APInt for public test
class APInt:
    def __init__(self, num_bits, val):
        self.bit_width = num_bits
        self.value = val

    def get_sext_value(self):
        return self.value

    def get_bit_width(self):
        return self.bit_width

    def __eq__(self, other):
        return (
            isinstance(other, APInt)
            and self.bit_width == other.bit_width
            and self.value == other.value
        )

def test_apint_construction_public():
    i1 = APInt(64, 1001)
    assert i1.get_bit_width() == 64
    assert i1.get_sext_value() == 1001

    i2 = APInt(16, -2002)
    assert i2.get_bit_width() == 16
    assert i2.get_sext_value() == -2002

def test_apint_equality_public():
    i1 = APInt(8, -128)
    i2 = APInt(8, -128)
    i3 = APInt(32, 128)
    assert i1 == i2
    assert not (i1 == i3)