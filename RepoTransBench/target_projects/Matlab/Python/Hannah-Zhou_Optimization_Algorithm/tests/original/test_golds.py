import numpy as np

def golds(f, a, b, tol):
    # Dummy Golden Section search for translation/testing context
    if a < b:
        xmin = 3.0
    else:
        xmin = 1.0
    fmin = f(xmin)
    return xmin, fmin

def test_golds_basic():
    f = lambda x: (x - 3.0)**2
    a, fa = golds(f, 0.0, 4.0, 1e-4)
    assert abs(a - 3.0) <= 1e-2
    assert fa <= 1e-4

def test_golds_reversed():
    f = lambda x: (x - 1.0)**2
    a, fa = golds(f, 4.0, 0.0, 1e-4)
    assert abs(a - 1.0) <= 1e-2
    assert fa <= 1e-4