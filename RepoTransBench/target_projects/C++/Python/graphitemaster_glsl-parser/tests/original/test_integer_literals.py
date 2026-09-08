import pytest

def test_integer_literals_and_assignments():
    test_uninitialized_int = None
    test_initialized_int = 42
    test_uninitialized_uint = None
    test_initialized_uint_no_suffix = 42
    test_initialized_uint_suffix = 42
    test_hex_no_suffix_upper = 255
    test_hex_suffix_upper = 255
    test_hex_no_suffix_lower = 255
    test_hex_suffix_lower = 255
    test_hex_no_suffix_mixed = 255
    test_hex_suffix_mixed = 255
    test_negative = -1
    test_octal = int('0777', 8)

    assert test_initialized_int == 42
    assert test_initialized_uint_no_suffix == 42
    assert test_initialized_uint_suffix == 42
    assert test_hex_no_suffix_upper == 255
    assert test_hex_suffix_upper == 255
    assert test_hex_no_suffix_lower == 255
    assert test_hex_suffix_lower == 255
    assert test_hex_no_suffix_mixed == 255
    assert test_hex_suffix_mixed == 255
    assert test_negative == -1
    assert test_octal == 511