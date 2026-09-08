import pytest
from src.neoeno_toy_project.lib import add

def test_add_basic_public():
    """
    Tests basic addition scenarios for public tests.
    Corresponds to C's test_add_basic_public.
    """
    assert add(3, 5) == 8
    assert add(-2, 2) == 0
    assert add(10, -10) == 0

def test_add_edge_cases_public():
    """
    Tests addition with edge cases for public tests, including large numbers.
    Corresponds to C's test_add_edge_cases_public.
    Python's integers handle arbitrary precision, so INT_MAX is not a strict limit,
    but the test scenario and values are preserved.
    """
    assert add(123456, 654321) == 777777
    assert add(-500, -500) == -1000
    assert add(1073741823, 1073741824) == 2147483647 # also INT_MAX for 32bit