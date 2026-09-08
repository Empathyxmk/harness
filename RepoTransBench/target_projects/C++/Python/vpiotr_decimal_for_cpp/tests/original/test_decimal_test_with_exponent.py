import pytest
from src.decimal.decimal import Decimal4, Decimal0

def test_decimal_with_exponent():
    # build positive values
    assert Decimal4.build_with_exponent(11, 0) == Decimal4("11")
    assert Decimal4.build_with_exponent(11, 2) == Decimal4("1100")
    assert Decimal4.build_with_exponent(11, -2) == Decimal4("0.11")
    assert Decimal4.build_with_exponent(11, 1) == Decimal4("110")
    assert Decimal4.build_with_exponent(11, -1) == Decimal4("1.1")

    # build negative values
    assert Decimal4.build_with_exponent(-11, 0) == Decimal4("-11")
    assert Decimal4.build_with_exponent(-11, 2) == Decimal4("-1100")
    assert Decimal4.build_with_exponent(-11, -2) == Decimal4("-0.11")
    assert Decimal4.build_with_exponent(-11, 1) == Decimal4("-110")
    assert Decimal4.build_with_exponent(-11, -1) == Decimal4("-1.1")

    # build zero
    assert Decimal4.build_with_exponent(0, -1) == Decimal4("0")
    assert Decimal4.build_with_exponent(0, 2) == Decimal4("0")
    assert Decimal4.build_with_exponent(0, 0) == Decimal4("0")

    # add, get, set
    temp = Decimal4.build_with_exponent(None, 111213, -3)
    assert temp == Decimal4("111.213")
    a = Decimal4()
    a.set_with_exponent(30, -2)
    temp += a
    assert temp == Decimal4("111.5130")

    m, e = temp.get_with_exponent()
    assert m == 111513
    assert e == -3

    # rounding
    temp = Decimal4()
    assert Decimal4.build_with_exponent(temp, 111213, -5) == Decimal4("1.1121")
    assert Decimal4.build_with_exponent(temp, 111215, -5) == Decimal4("1.1122")
    assert Decimal4.build_with_exponent(temp, -111213, -5) == Decimal4("-1.1121")
    assert Decimal4.build_with_exponent(temp, -111215, -5) == Decimal4("-1.1122")

    # check overflow
    assert Decimal0.build_with_exponent(1, 23) == Decimal0("0")
    assert Decimal4.build_with_exponent(1, 23) == Decimal4("0")
    assert Decimal4.build_with_exponent(1, 19) == Decimal4("0")
    assert Decimal4.build_with_exponent(1, 15) == Decimal4("0")

    # check underflow
    assert Decimal4.build_with_exponent(1, -19) == Decimal4("0")
    assert Decimal4.build_with_exponent(1, -15) == Decimal4("0")