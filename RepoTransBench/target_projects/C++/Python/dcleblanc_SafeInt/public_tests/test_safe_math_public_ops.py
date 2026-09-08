import pytest

def safe_add_int_int(a, b): return a + b
def safe_add_uint_uint(a, b): return a + b
def safe_add_uint_int(a, b): return a + b
def safe_add_int_uint(a, b): return a + b

def safe_mul_int_int(a, b): return a * b
def safe_mul_uint_uint(a, b): return a * b

def safe_div_int_int(a, b): return a // b
def safe_div_uint_uint(a, b): return a // b

def safe_sub_int_int(a, b): return a - b
def safe_sub_uint_uint(a, b): return a - b
def safe_sub_uint_int(a, b): return a - b
def safe_sub_int_uint(a, b): return a - b

def test_add_public():
    a, b = 7, 9
    ua, ub = 50, 82
    res = safe_add_int_int(a, b)
    assert res == 16

    ures = safe_add_uint_uint(ua, ub)
    assert ures == 132

    a, b = -23, 15
    res = safe_add_int_int(a, b)
    assert res == -8

    ua, a = 33, 44
    ures = safe_add_uint_int(ua, a)
    assert ures == 77

    ua, ub = 1000000, 2000000
    ures = safe_add_uint_uint(ua, ub)
    assert ures == 3000000

def test_mult_public():
    a, b = 4, 13
    res = safe_mul_int_int(a, b)
    assert res == 52

    ua, ub = 6, 100
    ures = safe_mul_uint_uint(ua, ub)
    assert ures == 600

    a, b = -7, -8
    res = safe_mul_int_int(a, b)
    assert res == 56

    ua, ub = 0, 200
    ures = safe_mul_uint_uint(ua, ub)
    assert ures == 0

    ua, ub = 1500, 3
    ures = safe_mul_uint_uint(ua, ub)
    assert ures == 4500

def test_div_public():
    a, b = 21, 3
    res = safe_div_int_int(a, b)
    assert res == 7

    ua, ub = 16, 2
    ures = safe_div_uint_uint(ua, ub)
    assert ures == 8

    a, b = 184, 1
    res = safe_div_int_int(a, b)
    assert res == 184

    a, b = -30, 5
    res = safe_div_int_int(a, b)
    assert res == -6

    ua, ub = 4000, 20
    ures = safe_div_uint_uint(ua, ub)
    assert ures == 200

def test_sub_public():
    a, b = 500, 300
    res = safe_sub_int_int(a, b)
    assert res == 200

    ua, ub = 900, 600
    ures = safe_sub_uint_uint(ua, ub)
    assert ures == 300

    a, b = -15, -5
    res = safe_sub_int_int(a, b)
    assert res == -10

    ua, a = 120, 30
    ures = safe_sub_uint_int(ua, a)
    assert ures == 90

    a, ua = 55, 60
    res = safe_sub_int_uint(a, ua)
    assert res == -5

def test_all_operation_publics():
    """ Top-level 'main' aggregator for coverage, not required for pytest, but to mirror C test """
    test_add_public()
    test_mult_public()
    test_div_public()
    test_sub_public()