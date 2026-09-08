from src.decimal.decimal import Decimal4, Decimal2, Decimal9

def test_decimal_rounding_basic_half_up():
    d = Decimal4("1.2345").round("half_up", 3)
    assert str(d) == "1.235"
    e = Decimal2("3.555").round("half_up", 2)
    assert str(e) == "3.56"
    f = Decimal9("42.123499999").round("half_up", 6)
    assert str(f) == "42.123500"

def test_decimal_rounding_truncate():
    d = Decimal4("9.8765").round("towards_zero", 2)
    assert str(d) == "9.87"
    e = Decimal4("-9.8765").round("towards_zero", 2)
    assert str(e) == "-9.87"

def test_decimal_rounding_floor_and_ceil():
    d = Decimal2("3.49").round("floor", 1)
    assert str(d) == "3.4"
    d = Decimal2("3.41").round("ceil", 1)
    assert str(d) == "3.5"
    d = Decimal2("-3.41").round("floor", 1)
    assert str(d) == "-3.5"
    d = Decimal2("-3.49").round("ceil", 1)
    assert str(d) == "-3.4"

def test_decimal_rounding_away_from_zero():
    d = Decimal4("1.1111").round("away_from_zero", 1)
    assert str(d) == "1.2"
    d = Decimal4("-1.1111").round("away_from_zero", 1)
    assert str(d) == "-1.2"

def test_decimal_rounding_zero_cases():
    d = Decimal4(0).round("half_up", 2)
    assert str(d) == "0.00" or str(d) == "0.0000"
    d = Decimal2(0).round("half_up", 2)
    assert str(d) == "0.00"
    d = Decimal9("0").round("half_up", 8)
    assert str(d) == "0.00000000"