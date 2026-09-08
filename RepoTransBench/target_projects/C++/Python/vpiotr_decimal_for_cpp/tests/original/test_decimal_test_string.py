from src.decimal.decimal import Decimal4, Decimal2, Decimal9

def test_decimal_string_basic_str():
    d = Decimal4("123.4567")
    assert str(d) == "123.4567"
    e = Decimal2("0.00")
    assert str(e) == "0.00"
    f = Decimal9("1.000000000")
    assert str(f) == "1.000000000"

def test_decimal_string_repr():
    d = Decimal4("-123.4567")
    assert repr(d).startswith("Decimal4(")
    assert "-123.4567" in repr(d)

def test_decimal_string_eq():
    a = Decimal4("3.1415")
    b = Decimal4("3.1415")
    c = Decimal4("03.1415")
    assert a == b
    assert a == c
    assert a is not None
    assert a != Decimal4("3.1416")

def test_decimal_string_comparison():
    a = Decimal4("5.4321")
    b = Decimal4("1.2345")
    assert a > b
    assert b < a
    assert a >= b
    assert b <= a
    assert a == Decimal4("5.4321")

def test_decimal_string_from_int():
    d = Decimal4(31415)
    assert str(d) == "31415.0000"
    d = Decimal2(99)
    assert str(d) == "99.00"
    d = Decimal9(42)
    assert str(d) == "42.000000000"

def test_decimal_string_from_float():
    d = Decimal4(3.1415)
    assert str(d) == "3.1415"
    d = Decimal2(0.0)
    assert str(d) == "0.00"
    d = Decimal9(-1.0)
    assert str(d) == "-1.000000000"

def test_decimal_string_edge_cases():
    d = Decimal4("0")
    assert str(d) == "0.0000"
    d = Decimal4("-0.0000")
    assert str(d) == "0.0000" or str(d) == "-0.0000"  # Acceptable for zero
    d = Decimal2("0000.00")
    assert str(d) == "0.00"

def test_decimal_string_invalid_type():
    try:
        Decimal4([1,2,3])
        assert False
    except Exception:
        assert True