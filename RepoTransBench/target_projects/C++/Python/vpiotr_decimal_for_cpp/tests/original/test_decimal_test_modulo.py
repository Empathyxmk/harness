from src.decimal.decimal import Decimal4, Decimal2, Decimal9

def test_decimal_modulo_basic():
    a = Decimal4("10.0000")
    b = Decimal4("3.0000")
    result = a % b
    assert str(result) == "1.0000"

    a = Decimal2("12.34")
    b = Decimal2("0.5")
    result = a % b
    assert str(result) == "0.34"

    a = Decimal9("123456789.123456789")
    b = Decimal9("100000000.000000007")
    result = a % b
    assert str(result) == "23456789.123456782"

def test_decimal_modulo_negative():
    a = Decimal4("-9.8756")
    b = Decimal4("2.0001")
    result = a % b
    # Check sign: In Python, sign of result follows b (divisor)
    # In C++/other: commonly sign follows dividend. 
    # Accept either, check mathematically valid
    res_val = float(str(result))
    assert abs(res_val - ((-9.8756) % 2.0001)) < 1e-4

    a = Decimal4("9.8756")
    b = Decimal4("-2.0001")
    result = a % b
    res_val = float(str(result))
    assert abs(res_val - (9.8756 % -2.0001)) < 1e-4

def test_decimal_modulo_zero_divisor_raises():
    a = Decimal2("5.00")
    try:
        _ = a % Decimal2("0.00")
        assert False
    except ZeroDivisionError:
        assert True

def test_decimal_modulo_larger_divisor():
    a = Decimal4("1.0000")
    b = Decimal4("2.0000")
    result = a % b
    assert str(result) == "1.0000"