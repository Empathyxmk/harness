from src.decimal.decimal import Decimal4, Decimal2, Decimal9

def test_decimal_basic_properties():
    d4 = Decimal4("1.2345")
    assert d4.digits == 4
    assert isinstance(d4.value, float) or isinstance(d4.value, int)
    d9 = Decimal9("1.000000000")
    assert d9.digits == 9

def test_decimal_str_repr():
    d = Decimal2("3.14")
    assert str(d) == "3.14"
    assert "Decimal2" in repr(d)
    assert "3.14" in repr(d)

def test_decimal_equality_and_comparison():
    a = Decimal4("0.01")
    b = Decimal4("0.01000")
    assert a == b
    assert not (a < a)
    assert a <= b
    assert a >= b
    assert not (a > b)
    assert not (a != b)

def test_decimal_creation_from_numeric_types():
    d1 = Decimal4(3)
    d2 = Decimal9(2.0)
    assert str(d1) == "3.0000"
    assert str(d2) == "2.000000000"
    d3 = Decimal2(0)
    assert str(d3) == "0.00"

def test_decimal_invalid_string():
    try:
        Decimal4("not_a_number")
        assert False
    except Exception:
        assert True

def test_decimal_hash_and_set():
    a = Decimal4("0.0100")
    b = Decimal4("0.01")
    s = set([a, b])
    assert len(s) == 1  # They are equal and should hash equal
    assert a in s
    assert b in s

def test_decimal_copy_and_clone():
    import copy
    d1 = Decimal4("1.2345")
    d2 = copy.copy(d1)
    d3 = copy.deepcopy(d1)
    assert d1 == d2
    assert d1 == d3
    assert d1 is not d2
    assert d1 is not d3