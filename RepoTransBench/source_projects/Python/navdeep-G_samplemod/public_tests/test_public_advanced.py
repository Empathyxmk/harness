from sample.core import safe_divide

def test_safe_divide_normal_public():
    # Different values from private test
    assert safe_divide(15, 3) == 5

def test_safe_divide_negative_public():
    assert safe_divide(-9, 3) == -3

def test_safe_divide_zero_dividend_public():
    assert safe_divide(0, 2) == 0

def test_safe_divide_raises_zero_division_public():
    try:
        safe_divide(2, 0)
        assert False, "Expected ZeroDivisionError"
    except ZeroDivisionError:
        assert True