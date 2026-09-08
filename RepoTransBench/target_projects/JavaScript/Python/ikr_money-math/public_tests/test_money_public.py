import pytest
import src.money as money

def test_amountToCents_positive_public():
    assert money.amountToCents("305.25") == "30525"

def test_amountToCents_negative_public():
    assert money.amountToCents("-12.34") == "-1234"

def test_amountToCents_just_cents_public():
    assert money.amountToCents("0.01") == "1"

def test_centsToAmount_positive_public():
    assert money.centsToAmount("507") == "5.07"

def test_centsToAmount_negative_public():
    assert money.centsToAmount("-20300") == "-203.00"

def test_centsToAmount_neg_fraction_public():
    assert money.centsToAmount("-56") == "-0.56"

def test_centsToAmount_tiny_neg_fraction_public():
    assert money.centsToAmount("-6") == "-0.06"

def test_centsToAmount_zero_public():
    assert money.centsToAmount("0") == "0.00"

def test_centsToAmount_small_positive_public():
    assert money.centsToAmount("7") == "0.07"

def test_centsToAmount_double_digit_public():
    assert money.centsToAmount("80") == "0.80"

def test_centsToAmount_undefined_public():
    assert money.centsToAmount() is None

def test_integralPart_positive_public():
    assert money.integralPart("853.20") == "853"

def test_integralPart_negative_public():
    assert money.integralPart("-75.15") == "-75"

def test_integralPart_zero_public():
    assert money.integralPart("0.00") == "0"

def test_format_chf_public():
    assert money.format("CHF", "1000.01") == "1,000.01"
    assert money.format("CHF", "-2589.50") == "-2,589.50"

def test_format_jpy_public():
    assert money.format("JPY", "870.00") == "870"
    assert money.format("JPY", "4625800.00") == "4,625,800"
    assert money.format("JPY", "-2500.00") == "-2,500"
    assert money.format("JPY", "-800000000.00") == "-800,000,000"

def test_format_eur_public():
    assert money.format("EUR", "311.00") == "311,00"
    assert money.format("EUR", "-412.00") == "-412,00"
    assert money.format("EUR", "-1501.10") == "-1.501,10"

def test_format_sek_public():
    assert money.format("SEK", "71.25") == "71,25"
    assert money.format("SEK", "-3339.00") == "-3 339,00"
    assert money.format("SEK", "-55555.55") == "-55 555,55"

def test_add_positive_public():
    assert money.add("20.15", "30.08") == "50.23"
    assert money.add("1234.56", "789.01") == "2023.57"
    assert money.add("4.44", "5.55") == "9.99"
    assert money.add("99.50", "0.50") == "100.00"