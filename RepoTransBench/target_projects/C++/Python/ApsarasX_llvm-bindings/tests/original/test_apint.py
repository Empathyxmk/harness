import pytest

# Dummy APInt, replace with correct implementation as needed
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

def test_apint_construction():
    i1 = APInt(32, 42)
    assert i1.get_bit_width() == 32
    assert i1.get_sext_value() == 42

    i2 = APInt(8, -5)
    assert i2.get_bit_width() == 8
    assert i2.get_sext_value() == -5

def test_apint_equality():
    i1 = APInt(16, 314)
    i2 = APInt(16, 314)
    i3 = APInt(32, 314)
    assert i1 == i2
    assert not (i1 == i3)