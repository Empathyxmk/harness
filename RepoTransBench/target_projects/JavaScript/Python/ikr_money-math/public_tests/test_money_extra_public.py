import pytest
import src.money as money

def test_floatToAmount_rounds_up_public():
    assert money.floatToAmount(12.345) == "12.35"
    assert money.floatToAmount(7.996) == "8.00"
    assert money.floatToAmount(7.935) == "7.94"
    assert money.floatToAmount(-2.574) == "-2.57"

def test_floatToAmount_scientific_public():
    assert money.floatToAmount(5e-5) == "0.00"
    assert money.floatToAmount(3.455e-1) == "0.35"

def test_floatToAmount_handles_string_values_public():
    assert money.floatToAmount("17.888") == "17.89"
    assert money.floatToAmount("-42.0587") == "-42.06"