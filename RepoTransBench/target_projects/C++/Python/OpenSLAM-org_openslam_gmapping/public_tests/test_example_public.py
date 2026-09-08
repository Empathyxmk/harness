import pytest
from src.example import Example

def test_add_basic_public():
    ex = Example()
    assert ex.add(4, 7) == 11
    assert ex.add(99, 1) == 100

def test_add_conditional_branch_public():
    ex = Example()
    assert ex.add(150, 20) == 130     # 150 > 100 -> 150-20=130
    assert ex.add(120, -10) == 130    # 120 > 100 -> 120-(-10)=130

def test_add_negative_numbers_public():
    ex = Example()
    assert ex.add(-6, 8) == 2         # -6 + 8 = 2
    assert ex.add(105, -5) == 110     # 105 > 100 -> 105-(-5)=110

def test_is_even_public():
    ex = Example()
    assert ex.isEven(8) is True
    assert ex.isEven(11) is False
    assert ex.isEven(-8) is True
    assert ex.isEven(-9) is False