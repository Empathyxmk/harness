import pytest
from src.placeholder import add

def test_add_simple_cases():
    # Simple tests for placeholder add function
    assert add(2, 2) == 4
    assert add(-1, 1) == 0
    assert add(0, 0) == 0
    assert add(-3, -7) == -10