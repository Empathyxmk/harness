import math
import pytest

from src.tinyexpr import compile as te_compile, free as te_free, TE_FUNCTION1

def test_basic_eval():
    err = [None]
    expr = te_compile("1+2*3", None, 0, err)
    assert expr is not None
    val = expr.eval()
    assert math.isclose(val, 7.0, abs_tol=1e-10)
    te_free(expr)

def test_error_handling():
    err = [None]
    expr = te_compile("1+", None, 0, err)
    assert expr is None
    assert err[0] != 0

def test_variables():
    x = 4.0
    vars = [("x", x)]
    err = [None]
    expr = te_compile("2*x", vars, 1, err)
    assert expr is not None
    val = expr.eval()
    assert math.isclose(val, 8.0, abs_tol=1e-10)
    te_free(expr)

def test_functions():
    vars = [
        ("sin", math.sin, TE_FUNCTION1),
        ("cos", math.cos, TE_FUNCTION1)
    ]
    err = [None]
    expr = te_compile("sin(0)+cos(0)", vars, 2, err)
    assert expr is not None
    val = expr.eval()
    assert math.isclose(val, 1.0, abs_tol=1e-10)
    te_free(expr)

def test_nan_and_inf():
    err = [None]
    expr_nan = te_compile("0/0", None, 0, err)
    assert expr_nan is not None
    val_nan = expr_nan.eval()
    assert math.isnan(val_nan)
    te_free(expr_nan)

    expr_inf = te_compile("1/0", None, 0, err)
    assert expr_inf is not None
    val_inf = expr_inf.eval()
    assert math.isinf(val_inf)
    te_free(expr_inf)

def test_parse_order_and_parenthesis():
    err = [None]
    expr = te_compile("(1+2)*3", None, 0, err)
    assert expr is not None
    val = expr.eval()
    assert math.isclose(val, 9.0, abs_tol=1e-10)
    te_free(expr)