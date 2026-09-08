import pytest

def test_dummy():
    """
    Translated from C's tests/unit/test_utils.c
    Original C test: ck_assert_int_eq(1, 1);
    """
    assert 1 == 1, "Dummy test failed!"