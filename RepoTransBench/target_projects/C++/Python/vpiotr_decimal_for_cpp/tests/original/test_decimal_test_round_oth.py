import pytest
from src.decimal.decimal import Decimal4, Decimal2, Decimal9

def test_decimal_round_oth_half_up():
    # Round half up
    a = Decimal4("1.2345")
    a.round("half_up", 3)
    assert str(a) == "1.235"
    b = Decimal2("1.555")
    b.round("half_up", 2)
    assert str(b) == "1.56"
    c = Decimal9("99.999999999")
    c.round("half_up", 0)
    assert str(c) == "100"

def test_decimal_round_oth_half_down():
    # Round half down
    a = Decimal4("1.2355")
    a.round("half_down", 3)
    assert str(a) == "1.235"
    b = Decimal2("1.555")
    b.round("half_down", 2)
    assert str(b) == "1.55"
    c = Decimal9("99.999999999")
    c.round("half_down", 0)
    assert str(c) == "99"

def test_decimal_round_oth_floor_and_ceil():
    # Floor and ceil
    a = Decimal4("1.9999")
    a.round("floor", 2)
    assert str(a) == "1.99"
    a.round("ceil", 2)
    assert str(a) == "2.00"
    b = Decimal2("-2.13")
    b.round("floor", 1)
    assert str(b) == "-2.2"
    b.round("ceil", 1)
    assert str(b) == "-2.1"
    c = Decimal4("0.1005")
    c.round("floor", 3)
    assert str(c) == "0.100"
    c.round("ceil", 3)
    assert str(c) == "0.101"

def test_decimal_round_oth_to_zero_and_away():
    # To zero and away from zero
    a = Decimal4("1.9876")
    a.round("towards_zero", 3)
    assert str(a) == "1.987"
    b = Decimal4("-1.2345")
    b.round("towards_zero", 2)
    assert str(b) == "-1.23"
    c = Decimal4("1.1111")
    c.round("away_from_zero", 1)
    assert str(c) == "1.2"
    d = Decimal4("-1.1111")
    d.round("away_from_zero", 1)
    assert str(d) == "-1.2"

def test_decimal_round_oth_invalid_strategy():
    a = Decimal4("1.2345")
    with pytest.raises(ValueError):
        a.round("unknown_strategy", 2)