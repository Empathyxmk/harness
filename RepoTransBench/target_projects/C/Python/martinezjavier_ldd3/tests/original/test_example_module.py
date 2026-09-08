import pytest
from src.martinezjavier_ldd3.example_module import add, max, abs_diff

def test_add_original():
    # Test add function
    assert add(1, 2) == 3
    assert add(-5, 5) == 0
    assert add(0, 0) == 0

def test_max_original():
    # Test max function
    assert max(1, 2) == 2
    assert max(7, 3) == 7
    assert max(-2, -5) == -2
    assert max(0, 0) == 0

def test_abs_diff_original():
    # Test abs_diff function
    assert abs_diff(10, 4) == 6   # 10 - 4 = 6
    assert abs_diff(3, 8) == 5    # 8 - 3 = 5
    assert abs_diff(7, 7) == 0    # 7 - 7 = 0