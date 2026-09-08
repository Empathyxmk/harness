import pytest

def apply_tuple(fn, tup):
    return fn(*tup)

def multiply(a, b, c):
    return a * b * c

def concat_with_dash(a, s, b):
    return str(a) + "-" + s + "-" + str(b)

class SubtractAll:
    def __call__(self, a, b, c):
        return a - b - c

def test_apply_tuple_multiply():
    t1 = (2, 4, 5)
    product = apply_tuple(multiply, t1)
    assert product == 40

def test_apply_tuple_concat_with_dash():
    t2 = (21, "xx", 88)
    result = apply_tuple(concat_with_dash, t2)
    assert result == "21-xx-88"

def test_apply_tuple_lambda_div():
    lambda_fn = lambda x, y: x / y
    t3 = (9.0, 3.0)
    r = apply_tuple(lambda_fn, t3)
    assert r == 3.0

def test_apply_tuple_functor_subtractall():
    s = SubtractAll()
    t4 = (30, 8, 10)
    diff = apply_tuple(s, t4)
    assert diff == 12