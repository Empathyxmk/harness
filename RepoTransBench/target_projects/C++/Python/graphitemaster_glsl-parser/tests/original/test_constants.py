import pytest

def test_constants_values():
    # These constants correspond to GLSL constant declarations
    test = 1.0
    test_neg = -1.0
    test_pos_two_sub = 2.0
    test_neg_two_sub = -2.0
    test_zero_add = 0.0

    assert test == 1.0
    assert test_neg == -1.0
    assert test_pos_two_sub == 2.0
    assert test_neg_two_sub == -2.0
    assert test_zero_add == 0.0