import pytest
import src.money as money

def test_amountToCents_positive():
    assert money.amountToCents("126.99") == "12699"

def test_amountToCents_negative():
    assert money.amountToCents("-10001.00") == "-1000100"

def test_amountToCents_just_cents_removes_zero():
    assert money.amountToCents("0.99") == "99"

def test_centsToAmount_positive():
    assert money.centsToAmount("2000010") == "20000.10"

def test_centsToAmount_negative():
    assert money.centsToAmount("-1000100") == "-10001.00"

def test_centsToAmount_neg_fraction():
    assert money.centsToAmount("-32") == "-0.32"

def test_centsToAmount_tiny_neg_fraction():
    assert money.centsToAmount("-1") == "-0.01"

def test_centsToAmount_zero():
    assert money.centsToAmount("0") == "0.00"

def test_centsToAmount_one():
    assert money.centsToAmount("1") == "0.01"

def test_centsToAmount_ten():
    assert money.centsToAmount("10") == "0.10"

def test_centsToAmount_undefined():
    assert money.centsToAmount() is None

def test_integralPart_positive():
    assert money.integralPart("12.00") == "12"

def test_integralPart_negative():
    assert money.integralPart("-55.10") == "-55"

def test_integralPart_zero():
    assert money.integralPart("0.00") == "0"

def test_format_chf():
    assert money.format("CHF", "560.05") == "560.05"
    assert money.format("CHF", "-1560.00") == "-1,560.00"

def test_format_jpy():
    assert money.format("JPY", "560.00") == "560"
    assert money.format("JPY", "236800.00") == "236,800"
    assert money.format("JPY", "-1000000000.00") == "-1,000,000,000"
    assert money.format("JPY", "-100000000000.00") == "-100,000,000,000"

def test_format_eur():
    assert money.format("EUR", "560.00") == "560,00"
    assert money.format("EUR", "-1560.00") == "-1.560,00"
    assert money.format("EUR", "-100000000000.00") == "-100.000.000.000,00"

def test_format_sek():
    assert money.format("SEK", "560.00") == "560,00"
    assert money.format("SEK", "-1560.00") == "-1 560,00"
    assert money.format("SEK", "-100000000000.00") == "-100 000 000 000,00"

def test_add_decimals_1():
    assert money.add("16.11", "17.07") == "33.18"

def test_add_decimals_2():
    assert money.add("65535.79", "1024.85") == "66560.64"

def test_add_decimals_3():
    assert money.add("1.99", "0.02") == "2.01"

def test_add_decimals_4():
    assert money.add("1.90", "0.10") == "2.00"