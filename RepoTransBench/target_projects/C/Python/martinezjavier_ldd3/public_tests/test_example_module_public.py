import pytest
from src.martinezjavier_ldd3.example_module import add, max, abs_diff

def test_add_public():
    # Test add function with different data
    assert add(6, 4) == 10
    assert add(-3, -2) == -5
    assert add(100, 200) == 300

def test_max_public():
    # Test max function with different data
    assert max(0, -1) == 0
    assert max(15, 20) == 20
    assert max(-10, -20) == -10
    assert max(100, 100) == 100

def test_abs_diff_public():
    # Test abs_diff function with different data
    assert abs_diff(50, 45) == 5   # 50 - 45 = 5
    assert abs_diff(-6, 5) == 11   # 5 - (-6) = 11
    assert abs_diff(0, 100) == 100 # 100 - 0 = 100