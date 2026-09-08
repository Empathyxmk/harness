import pytest
from src.mozillazg_cloud_native_security_with_ebpf.example import add, is_even, division

def test_add():
    assert add(1, 2) == 3
    assert add(-3, 2) == -1
    assert add(0, 0) == 0
    assert add(10, 10) == 20

def test_is_even():
    assert is_even(4) == 1
    assert is_even(7) == 0
    assert is_even(0) == 1
    assert is_even(-3) == 0

def test_division():
    assert division(6, 3) == 2
    assert division(1, 0) == -1  # divided by zero
    assert division(0, 5) == 0
    assert division(-10, 5) == -2