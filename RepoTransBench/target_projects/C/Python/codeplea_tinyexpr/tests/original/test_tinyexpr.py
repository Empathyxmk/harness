import math
import pytest

from src.tinyexpr import interp as te_interp, compile as te_compile, free as te_free, TE_FUNCTION1, TE_FUNCTION2

# Helpers for custom functions
def custom_add(a, b): return a + b
def custom_neg(a): return -a

varval = 42.5

def test_constants_and_basic_arith():
    err = [None]
    assert math.isclose(te_interp("1", err), 1.0, abs_tol=1e-6)
    assert err[0] == 0

    assert math.isclose(te_interp("3+4*2-1/5", err), 3 + 4*2 - 1.0/5, abs_tol=1e-6)
    assert err[0] == 0

    assert math.isclose(te_interp("(2+3)*(5-1)", err), (2+3)*(5-1), abs_tol=1e-6)
    assert err[0] == 0

def test_functions_and_variables():
    err = [None]
    vars = [
        ("x", varval),
        ("add", custom_add, TE_FUNCTION2),
        ("neg", custom_neg, TE_FUNCTION1),
    ]
    assert math.isclose(te_interp("sin(pi/2)", err), 1.0, abs_tol=1e-6)
    assert err[0] == 0

    assert math.isclose(te_interp("log(e)", err), 1.0, abs_tol=1e-6)
    assert err[0] == 0

    assert math.isclose(te_interp("add(5,7)", err), 12.0, abs_tol=1e-6)
    assert err[0] == 0

    expr = te_compile("x+8", vars, 1, err)
    assert expr is not None
    assert math.isclose(expr.eval(), varval+8.0, abs_tol=1e-6)
    te_free(expr)

    expr = te_compile("neg(-5)", vars, 3, err)
    assert expr is not None
    assert math.isclose(expr.eval(), 5.0, abs_tol=1e-6)
    te_free(expr)

def test_errors_and_edge_cases():
    err = [None]

    # Unmatched parentheses
    expr = te_compile("((1+2)", None, 0, err)
    assert expr is None
    assert err[0] != 0

    # Invalid variable
    expr = te_compile("foobar", None, 0, err)
    assert expr is None
    assert err[0] != 0

    # Division by zero (should evaluate to INF or error)
    expr = te_compile("5/0", None, 0, err)
    assert expr is not None
    d = expr.eval()
    assert math.isinf(d)
    te_free(expr)

    # Empty string
    expr = te_compile("", None, 0, err)
    assert expr is None

    # NULL string (None)
    expr = te_compile(None, None, 0, err)
    assert expr is None