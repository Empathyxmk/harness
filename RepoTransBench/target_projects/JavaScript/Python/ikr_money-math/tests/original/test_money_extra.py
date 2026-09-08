import pytest
import src.money as money

def test_floatToAmount_positive_less_than_three_decimals():
    assert money.floatToAmount(1.23) == "1.23"
    assert money.floatToAmount(123) == "123.00"
    assert money.floatToAmount(0.4) == "0.40"

def test_floatToAmount_rounding_up():
    assert money.floatToAmount(1.226) == "1.23"
    assert money.floatToAmount(123.005) == "123.01"
    assert money.floatToAmount(-1.226) == "-1.23"

def test_floatToAmount_scientific_notation_small():
    assert money.floatToAmount(1e-2) == "0.01"
    assert money.floatToAmount(-2.5e-2) == "-0.02"

def test_floatToAmount_unusual_format_string():
    assert isinstance(money.floatToAmount("0.01"), str)

def test_centsToAmount_not_string_returns_undefined():
    assert money.centsToAmount(1234) is None
    assert money.centsToAmount(None) is None
    assert money.centsToAmount({}) is None

def test_add_sub_negative_values():
    assert money.add("-1.00", "-2.00") == "-3.00"

def test_add_positive_negative():
    assert money.add("5.00", "-2.00") == "3.00"

import pytest

@pytest.mark.parametrize("ccy", ["LTL", "PLN", "SKK", "UAH"])
def test_format_currency_space_thousands(ccy):
    assert money.format(ccy, "12345.67") == "12 345,67"
    assert money.format(ccy, "-5678.01") == "-5 678,01"

def test_format_unknown_currency_returns_amount():
    assert money.format("XXX", "123.45") == "123.45"

def test_amountToCents_negative_under_ten_cents():
    assert money.amountToCents("-5.03") == "-503"