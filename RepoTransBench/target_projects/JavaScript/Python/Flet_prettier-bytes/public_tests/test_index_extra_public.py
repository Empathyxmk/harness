import pytest
from flet_prettier_bytes import prettier_bytes

class TestPrettierBytesPublicEdgeCases:
    def test_negative_number_between_minus1_and_0(self):
        assert prettier_bytes(-0.4) == '-0.4 B'
        assert prettier_bytes(-0.01) == '-0.01 B'

    def test_other_negative_bytes(self):
        assert prettier_bytes(-77) == '-77 B'
        assert prettier_bytes(-2345) == '-2.3 KB'
        assert prettier_bytes(-3500) == '-3.5 KB'
        assert prettier_bytes(-1900) == '-1.9 KB'

    def test_zero_bytes_alternate(self):
        assert prettier_bytes(0) == '0 B'
        assert prettier_bytes(-0) == '0 B'

    def test_no_unit_if_just_below_1000(self):
        assert prettier_bytes(999) == '999 B'
        assert prettier_bytes(-999) == '-999 B'

    def test_threshold_1000_other_values(self):
        assert prettier_bytes(1500) == '1.5 KB'
        assert prettier_bytes(123456) == '123 KB'
        assert prettier_bytes(9000) == '9 KB'

    def test_large_units_other_magnitudes(self):
        assert prettier_bytes(2e21) == '2 ZB'
        assert prettier_bytes(7.6e18) == '7.6 EB'
        assert prettier_bytes(2.4e15) == '2.4 PB'
        assert prettier_bytes(1.2e12) == '1.2 TB'
        assert prettier_bytes(4.7e9) == '4.7 GB'
        assert prettier_bytes(6.5e6) == '6.5 MB'

    def test_decimal_rounding_public_examples(self):
        assert prettier_bytes(5023) == '5.0 KB'
        assert prettier_bytes(2591) == '2.6 KB'

    def test_infinity_and_minus_infinity(self):
        assert prettier_bytes(float("inf")) == 'Infinity YB'
        assert prettier_bytes(float("-inf")) == '-Infinity YB'

    @pytest.mark.parametrize('bad_input', ['hello', None, {}, [],]) # python has no undefined
    def test_bad_types_public_set(self, bad_input):
        with pytest.raises(TypeError):
            prettier_bytes(bad_input)