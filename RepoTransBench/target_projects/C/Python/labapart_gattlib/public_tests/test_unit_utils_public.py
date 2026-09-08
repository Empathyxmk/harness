import pytest

def test_always_true():
    """
    Translated from C's tests/unit/test_utils_public.c
    Original C test: ck_assert_int_eq(2, 2);
    """
    assert 2 == 2, "Public dummy test failed!"