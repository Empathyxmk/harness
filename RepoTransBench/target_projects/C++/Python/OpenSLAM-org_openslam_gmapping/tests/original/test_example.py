import pytest
from src.example import Example

def test_add_basic():
    ex = Example()
    assert ex.add(1, 2) == 3
    assert ex.add(100, 50) == 150

def test_add_conditional_branch():
    ex = Example()
    assert ex.add(101, 5) == 96       # 101 > 100 -> 101-5=96
    assert ex.add(200, 100) == 100    # 200 > 100 -> 200-100=100

def test_add_negative_numbers():
    ex = Example()
    assert ex.add(-3, 5) == 2         # -3 + 5 = 2 (not > 100)
    assert ex.add(102, -3) == 105     # 102 > 100 -> 102-(-3)=105

def test_is_even():
    ex = Example()
    assert ex.isEven(2) is True
    assert ex.isEven(3) is False
    assert ex.isEven(0) is True
    assert ex.isEven(-4) is True
    assert ex.isEven(-5) is False