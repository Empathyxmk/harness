import pytest
from src.decimal.decimal import Decimal4, Decimal2, Decimal9

def test_decimal_arithmetic_addition():
    assert Decimal4("1.1") + Decimal4("1.2") == Decimal4("2.3")
    assert Decimal2("0.5") + Decimal2("0.5") == Decimal2("1.0")
    assert Decimal4("1.2345") + Decimal4("2.3456") == Decimal4("3.5801")
    assert Decimal9("1.1") + Decimal9("2.2") == Decimal9("3.3")
    assert Decimal2("0") + Decimal2("0") == Decimal2("0")
    assert Decimal9("-1.2") + Decimal9("1.2") == Decimal9("0.0")

def test_decimal_arithmetic_subtraction():
    assert Decimal4("1.1") - Decimal4("0.2") == Decimal4("0.9")
    assert Decimal2("0.5") - Decimal2("0.2") == Decimal2("0.3")
    assert Decimal4("2.3456") - Decimal4("1.2345") == Decimal4("1.1111")
    assert Decimal9("3.3") - Decimal9("2.2") == Decimal9("1.1")
    assert Decimal2("0") - Decimal2("0") == Decimal2("0")
    assert Decimal9("-1.2") - Decimal9("1.2") == Decimal9("-2.4")

def test_decimal_arithmetic_negation():
    assert -Decimal4("1.1") == Decimal4("-1.1")
    assert -Decimal2("0.5") == Decimal2("-0.5")
    assert -Decimal4("0.0") == Decimal4("0.0")
    assert -Decimal9("-3.3") == Decimal9("3.3")