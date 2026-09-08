import unittest
from paramformatter import mixed_frac_inch

class DummyUnitsManager:
    def convert(self, value, from_unit, to_unit):
        # For test, just return the input value unchanged.
        return value

class DummyParam:
    def __init__(self, value, unit):
        self.value = value
        self.unit = unit

class DummyDesign:
    def __init__(self):
        self.fusionUnitsManager = DummyUnitsManager()

class TestMixedFracInch(unittest.TestCase):
    def setUp(self):
        self.design = DummyDesign()

    def test_unitless_positive(self):
        p = DummyParam(1.75, '')
        self.assertEqual(mixed_frac_inch(p, self.design), '1 3/4"')

    def test_unitless_negative(self):
        p = DummyParam(-2.5, '')
        self.assertEqual(mixed_frac_inch(p, self.design), '-2 1/2"')

    def test_unit_inch(self):
        p = DummyParam(2.5, 'in')
        # Should use units manager, but here conversion returns value unchanged
        self.assertEqual(mixed_frac_inch(p, self.design), '2 1/2"')

    def test_whole_number(self):
        p = DummyParam(3.0, '')
        self.assertEqual(mixed_frac_inch(p, self.design), '3"')
        p = DummyParam(0.0, '')
        self.assertEqual(mixed_frac_inch(p, self.design), '0"')

    def test_fraction_only(self):
        p = DummyParam(0.25, '')
        self.assertEqual(mixed_frac_inch(p, self.design), '1/4"')
        p = DummyParam(-0.75, '')
        self.assertEqual(mixed_frac_inch(p, self.design), '-3/4"')

    def test_zero(self):
        p = DummyParam(0, '')
        self.assertEqual(mixed_frac_inch(p, self.design), '0"')