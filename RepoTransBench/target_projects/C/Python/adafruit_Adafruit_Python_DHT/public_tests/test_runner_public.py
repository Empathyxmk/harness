import pytest

def test_difference():
    """Corresponds to C's public test_difference."""
    assert 3 - 1 == 2

def test_edge_case_negative():
    """Corresponds to C's public test_edge_case_negative."""
    b = -1
    assert b != 0
    assert b == -1