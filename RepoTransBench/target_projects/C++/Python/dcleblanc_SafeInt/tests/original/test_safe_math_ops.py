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

def test_add_original():
    a, b = 1, 2
    ua, ub = 3, 4
    res = safe_add_int_int(a, b)
    assert res == 3
    ures = safe_add_uint_uint(ua, ub)
    assert ures == 7
    a, b = -1, 5
    res = safe_add_int_int(a, b)
    assert res == 4
    ua, a = 4, -3
    ures = safe_add_uint_int(ua, a)
    assert ures == 1

def test_mult_original():
    a, b = 3, 2
    res = safe_mul_int_int(a, b)
    assert res == 6
    ua, ub = 4, 5
    ures = safe_mul_uint_uint(ua, ub)
    assert ures == 20
    a, b = -7, 2
    res = safe_mul_int_int(a, b)
    assert res == -14
    ua, ub = 0, 10
    ures = safe_mul_uint_uint(ua, ub)
    assert ures == 0

def test_div_original():
    a, b = 8, 2
    res = safe_div_int_int(a, b)
    assert res == 4
    ua, ub = 9, 3
    ures = safe_div_uint_uint(ua, ub)
    assert ures == 3
    a, b = -12, 4
    res = safe_div_int_int(a, b)
    assert res == -3
    ua, ub = 10, 5
    ures = safe_div_uint_uint(ua, ub)
    assert ures == 2

def test_sub_original():
    a, b = 10, 5
    res = safe_sub_int_int(a, b)
    assert res == 5
    ua, ub = 15, 4
    ures = safe_sub_uint_uint(ua, ub)
    assert ures == 11
    a, b = -3, -7
    res = safe_sub_int_int(a, b)
    assert res == 4
    ua, a = 8, 3
    ures = safe_sub_uint_int(ua, a)
    assert ures == 5
    a, ua = 6, 12
    res = safe_sub_int_uint(a, ua)
    assert res == -6

def test_all_operation_originals():
    test_add_original()
    test_mult_original()
    test_div_original()
    test_sub_original()