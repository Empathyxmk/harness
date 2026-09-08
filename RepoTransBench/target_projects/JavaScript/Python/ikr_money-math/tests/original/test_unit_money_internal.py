import pytest
import src.money as Money

def test_format_unknown_currency():
    assert Money.format("XXX", "1234567.89") == "1234567.89"

def test_amountToCents_strips_dot_and_zeros():
    assert Money.amountToCents("00123.45") == "12345"
    assert Money.amountToCents("0.01") == "1"
    assert Money.amountToCents("123.45") == "12345"
    assert Money.amountToCents("000.00") == ""

def test_centsToAmount_returns_undefined_for_nonstring():
    assert Money.centsToAmount(123) is None
    assert Money.centsToAmount(None) is None
    assert Money.centsToAmount() is None
    assert Money.centsToAmount({}) is None

def test_centsToAmount_negative_and_small():
    assert Money.centsToAmount("-1") == "-0.01"
    assert Money.centsToAmount("-12") == "-0.12"
    assert Money.centsToAmount("-123") == "-1.23"
    assert Money.centsToAmount("1") == "0.01"
    assert Money.centsToAmount("12") == "0.12"
    assert Money.centsToAmount("123456") == "1234.56"

def test_floatToAmount_rounds_and_large():
    assert Money.floatToAmount(1.005) == "1.01"
    assert Money.floatToAmount(1.004) == "1.00"
    assert Money.floatToAmount(3) == "3.00"
    assert Money.floatToAmount(0.1) == "0.10"
    assert Money.floatToAmount(-1.999) == "-2.00"
    assert Money.floatToAmount(1e2) == "100.00"
    assert Money.floatToAmount(-1.996) == "-2.00"

def test_integralPart_no_decimals():
    assert Money.integralPart("123.45") == "123"
    assert Money.integralPart("-99.10") == "-99"

def test_format_dispatches_to_currency():
    assert Money.format("USD", "12345.67") == "12,345.67"
    assert Money.format("EUR", "12345.67") == "12.345,67"
    assert Money.format("SEK", "12345.67") == "12 345,67"
    assert Money.format("JPY", "12345.67") == "12,345"
    assert Money.format("GBP", "12345.67") == "12.345,67"
    assert Money.format("CHF", "12345.67") == "12,345.67"
    assert Money.format("LTL", "12345.67") == "12 345,67"
    assert Money.format("PLN", "12345.67") == "12 345,67"
    assert Money.format("SKK", "12345.67") == "12 345,67"
    assert Money.format("UAH", "12345.67") == "12 345,67"

def test_add_sub_mul_div():
    assert Money.add("1.00", "1.00") == "2.00"
    assert Money.subtract("2.00", "0.50") == "1.50"
    assert Money.mul("2.00", "3.00") == "6.00"
    assert Money.mul("2.25", "2.00") == "4.50"
    assert Money.div("6.00", "2.00") == "3.00"
    assert Money.div("7.00", "2.00") == "3.50"
    assert Money.div("1.00", "3.00") == "0.33"
    assert Money.mul("999.99", "0.01") == "10.00"

def test_percent_rounding_and_edges():
    assert Money.percent("100.00", "50.00") == "50.00"
    assert Money.percent("100.00", "23.45") == "23.45"
    assert Money.percent("1.00", "99.99") == "1.00"
    assert Money.percent("1.00", "99.98") == "1.00"

def test_roundUpTo5Cents_variants():
    assert Money.roundUpTo5Cents("1.01") == "1.05"
    assert Money.roundUpTo5Cents("1.02") == "1.05"
    assert Money.roundUpTo5Cents("1.03") == "1.05"
    assert Money.roundUpTo5Cents("1.04") == "1.05"
    assert Money.roundUpTo5Cents("1.05") == "1.05"
    assert Money.roundUpTo5Cents("21.10") == "21.10"
    assert Money.roundUpTo5Cents("21.13") == "21.15"
    assert Money.roundUpTo5Cents("21.17") == "21.20"

def test_roundTo5Cents_logic():
    assert Money.roundTo5Cents("1.03") == "1.05"
    assert Money.roundTo5Cents("1.02") == "1.00"
    assert Money.roundTo5Cents("2.08") == "2.10"
    assert Money.roundTo5Cents("2.04") == "2.05"

def test_cmp_isEqual_isZero_isNeg_isPos():
    assert Money.cmp("3.00", "2.00") > 0
    assert Money.cmp("2.00", "2.00") == 0
    assert Money.cmp("1.00", "2.00") < 0
    assert Money.isEqual("2.00", "2.00") is True
    assert Money.isZero("0.00") is True
    assert Money.isZero("0.01") is False
    assert Money.isNegative("-1.00") is True
    assert Money.isNegative("0.00") is False
    assert Money.isPositive("2.00") is True
    assert Money.isPositive("-2.00") is False

def test_isGreater_isGTE_isLT_isLTE():
    assert Money.isGreaterThan("2.00", "1.00") is True
    assert Money.isGreaterOrEqualTo("2.00", "2.00") is True
    assert Money.isGreaterOrEqualTo("3.00", "2.00") is True
    assert Money.isLessThan("2.00", "3.00") is True
    assert Money.isLessThan("3.00", "3.00") is False
    assert Money.isLessOrEqualTo("3.00", "3.00") is True
    assert Money.isLessOrEqualTo("2.00", "3.00") is True