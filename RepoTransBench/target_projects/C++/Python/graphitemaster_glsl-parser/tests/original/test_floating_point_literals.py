import pytest

def test_floating_point_literals():
    # Test for initialization and value check
    test_float_uninitialized = None
    test_float_initialized = 1.5
    test_float_f_lower = 1.5
    test_float_f_upper = 1.5
    test_double_uininitialized = None
    test_double_initialized = 1.5
    test_double_lf_lower = 1.5
    test_double_lf_upper = 1.5
    test_float_f_zero = 1.0

    assert test_float_initialized == 1.5
    assert test_float_f_lower == 1.5
    assert test_float_f_upper == 1.5
    assert test_double_initialized == 1.5
    assert test_double_lf_lower == 1.5
    assert test_double_lf_upper == 1.5
    assert test_float_f_zero == 1.0