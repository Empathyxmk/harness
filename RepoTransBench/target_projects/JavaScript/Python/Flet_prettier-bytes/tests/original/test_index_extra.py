import pytest
from flet_prettier_bytes import prettier_bytes

class TestPrettierBytesEdgeCases:
    # Negative numbers
    def test_negative_number_below_1(self):
        assert prettier_bytes(-0.2) == '-0.2 B'

    def test_negative_bytes(self):
        assert prettier_bytes(-45) == '-45 B'
        assert prettier_bytes(-1500) == '-1.5 KB'
        assert prettier_bytes(-2510) == '-2.5 KB'
        assert prettier_bytes(-1000) == '-1 KB'

    # Zero
    def test_zero_bytes(self):
        assert prettier_bytes(0) == '0 B'

    # Numbers just less than 1000
    def test_no_unit_if_under_1000(self):
        assert prettier_bytes(999) == '999 B'

    # Numbers just above 1000
    def test_threshold_1000(self):
        assert prettier_bytes(1000) == '1 KB'
        assert prettier_bytes(1001) == '1.0 KB'
        assert prettier_bytes(1500) == '1.5 KB'
        assert prettier_bytes(1100) == '1.1 KB'
        assert prettier_bytes(2000) == '2 KB'
        assert prettier_bytes(9900) == '9.9 KB'
        assert prettier_bytes(10000) == '10 KB'

    # Large numbers to hit higher units
    def test_large_units(self):
        assert prettier_bytes(1e24) == '1 YB'
        assert prettier_bytes(1e21) == '1 ZB'
        assert prettier_bytes(1e18) == '1 EB'
        assert prettier_bytes(1e15) == '1 PB'
        assert prettier_bytes(1e12) == '1 TB'
        assert prettier_bytes(1e9) == '1 GB'
        assert prettier_bytes(1e6) == '1 MB'
        assert prettier_bytes(1e3) == '1 KB'

    # Decimal handling: just above/below thresholds for decimals
    def test_decimal_rounding(self):
        assert prettier_bytes(1234) == '1.2 KB'
        assert prettier_bytes(12345) == '12 KB'
        assert prettier_bytes(10000) == '10 KB'
        assert prettier_bytes(10100) == '10 KB'
        assert prettier_bytes(10900) == '11 KB'
        assert prettier_bytes(100900) == '101 KB'

    # Special numbers: Infinity is valid input, should NOT throw
    def test_infinity_returns_value(self):
        assert prettier_bytes(float('inf')) == 'Infinity YB'
        assert prettier_bytes(float('-inf')) == '-Infinity YB'

    # non-number, null, object, array
    @pytest.mark.parametrize('bad_input', [None, {}, [], False])
    def test_non_number_argument_types(self, bad_input):
        with pytest.raises(TypeError):
            prettier_bytes(bad_input)