import pytest
import src.money as Money

def test_floatToAmount_rounds_large_floats_public():
    assert Money.floatToAmount(13.987) == "13.99"
    assert Money.floatToAmount(-99.991) == "-99.99"
    assert Money.floatToAmount(750.324) == "750.32"
    assert Money.floatToAmount("55") == "55.00"
    assert Money.floatToAmount(8) == "8.00"
    assert Money.floatToAmount(0.45) == "0.45"
    assert Money.floatToAmount(-16.995) == "-16.99"
    assert Money.floatToAmount(2e2) == "200.00"
    assert Money.floatToAmount(-16.996) == "-17.00"

def test_floatToAmount_returns_string_type_public():
    assert isinstance(Money.floatToAmount(25.713), str)
    assert isinstance(Money.floatToAmount(-1.22), str)

def test_floatToAmount_rounding_boundaries_public():
    assert Money.floatToAmount(33.435) == "33.44"
    # -32.945 round same as JS: "-32.94"
    assert Money.floatToAmount(-32.945) == "-32.94"