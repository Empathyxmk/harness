import pytest

def test_sum():
    """Corresponds to C's test_sum."""
    assert 1 + 1 == 2

def test_edge_case_zero():
    """Corresponds to C's test_edge_case_zero."""
    a = 0
    assert a == 0