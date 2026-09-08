import pytest
from src.neoeno_toy_project.lib import add

def test_add_basic():
    """
    Tests basic addition scenarios.
    Corresponds to C's test_add_basic.
    """
    assert add(1, 2) == 3
    assert add(0, 0) == 0
    assert add(-1, -1) == -2

def test_add_edge_cases():
    """
    Tests addition with edge cases including large numbers.
    Corresponds to C's test_add_edge_cases.
    Python's integers handle arbitrary precision, so INT_MAX is not a strict limit,
    but the test scenario and values are preserved.
    """
    assert add(1000000, 1) == 1000001
    assert add(-1000, 1000) == 0
    assert add(2147483640, 7) == 2147483647 # INT_MAX for 32bit