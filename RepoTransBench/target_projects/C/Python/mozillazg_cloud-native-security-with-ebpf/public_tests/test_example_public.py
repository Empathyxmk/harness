import pytest
from src.mozillazg_cloud_native_security_with_ebpf.example import add, is_even, division

def test_add():
    assert add(4, 7) == 11
    assert add(60, 40) == 100
    assert add(-4, -5) == -9
    assert add(50, -25) == 25

def test_is_even():
    assert is_even(102) == 1
    assert is_even(11) == 0
    assert is_even(-8) == 1
    assert is_even(101) == 0

def test_division():
    assert division(25, 5) == 5
    assert division(0, 0) == -1
    assert division(8, 20) == 0  # integer division (8 // 20 = 0)
    assert division(9, -3) == -3