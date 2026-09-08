import pytest
from src.decimal.decimal import Decimal3

def test_decimal_basic_public():
    # Different data: 271828 (e-ish) with 3 decimals
    value1 = Decimal3(271828)
    value2 = Decimal3("271828")
    assert value1 == value2