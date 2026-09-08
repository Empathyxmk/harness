import math

import pytest

from src.tinyexpr import interp as te_interp, compile as te_compile, free as te_free

def test_simple_public():
    err = [None]
    assert abs(te_interp("2*5+1", err) - 11) < 1e-10 and err[0] == 0
    assert abs(te_interp("100/4-6", err) - 19) < 1e-10 and err[0] == 0
    assert abs(te_interp("5^4", err) - 625) < 1e-10 and err[0] == 0
    assert abs(te_interp("sqrt(225)", err) - 15.0) < 1e-10 and err[0] == 0
    assert abs(te_interp("abs(-1234)", err) - 1234.0) < 1e-10 and err[0] == 0

def test_variables_public():
    a = 4
    b = 9
    err = [None]
    vars = [
        ("a", a, 0, 0),
        ("b", b, 0, 0)
    ]
    expr = te_compile("a*b+2", vars, 2, err)
    assert err[0] == 0
    assert abs(expr.eval() - (a*b+2)) < 1e-10
    te_free(expr)

    expr = te_compile("b/a-0.5", vars, 2, err)
    assert err[0] == 0
    assert abs(expr.eval() - (b/a-0.5)) < 1e-10
    te_free(expr)

def test_functions_public():
    err = [None]
    assert abs(te_interp("cos(0)", err) - 1.0) < 1e-10 and err[0] == 0
    assert abs(te_interp("tan(pi/4)", err) - 1.0) < 1e-10 and err[0] == 0
    assert abs(te_interp("log(1)", err) - 0.0) < 1e-10 and err[0] == 0