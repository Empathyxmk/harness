import pytest
from src.decimal.decimal import Decimal4

def test_decimal_utils_str_repr_eq():
    val1 = Decimal4("1.1234")
    val2 = Decimal4("1.1234")
    val3 = Decimal4("2.5678")
    assert str(val1) == "1.1234"
    assert repr(val1) == "Decimal4('1.1234')"
    assert val1 == val2
    assert val1 != val3

def test_decimal_utils_clone():
    a = Decimal4("8.3333")
    b = a.clone()
    assert a == b
    b += Decimal4("0.6667")
    assert b == Decimal4("9.0000")
    assert a == Decimal4("8.3333")