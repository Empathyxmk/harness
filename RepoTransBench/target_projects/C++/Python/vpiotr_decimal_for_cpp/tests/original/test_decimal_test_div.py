import pytest
from src.decimal.decimal import Decimal4, Decimal2, Decimal9

def test_decimal_div_basic():
    assert Decimal4("2.0") / Decimal4("2.0") == Decimal4("1.0")
    assert Decimal2("1.5") / Decimal2("0.5") == Decimal2("3.0")
    assert Decimal4("4.8") / Decimal4("2.4") == Decimal4("2.0")
    assert Decimal9("9.0") / Decimal9("3.0") == Decimal9("3.0")

def test_decimal_div_one_divided():
    assert Decimal4("1.0") / Decimal4("2.0") == Decimal4("0.5")
    assert Decimal2("1.0") / Decimal2("4.0") == Decimal2("0.25")
    assert Decimal4("1.0") / Decimal4("10.0") == Decimal4("0.1")
    assert Decimal9("1.0") / Decimal9("3.0") == Decimal9("0.333333333")

def test_decimal_div_negative():
    assert Decimal4("-4.8") / Decimal4("2.4") == Decimal4("-2.0")
    assert Decimal9("9.0") / Decimal9("-3.0") == Decimal9("-3.0")
    assert Decimal4("-2.0") / Decimal4("-2.0") == Decimal4("1.0")

def test_decimal_div_zero_dividend():
    assert Decimal4("0.0") / Decimal4("2.0") == Decimal4("0.0")
    assert Decimal9("0.0") / Decimal9("3.0") == Decimal9("0.0")

def test_decimal_div_raises_zero_division():
    with pytest.raises(ZeroDivisionError):
        _ = Decimal4("7.7") / Decimal4("0.0")
    with pytest.raises(ZeroDivisionError):
        _ = Decimal2("-3.1") / Decimal2("0.0")
    with pytest.raises(ZeroDivisionError):
        _ = Decimal9("5.5") / Decimal9("0.0")