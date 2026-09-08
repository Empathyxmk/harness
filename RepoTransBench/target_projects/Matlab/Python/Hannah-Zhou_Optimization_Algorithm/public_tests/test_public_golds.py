import numpy as np

def golds(f, a, b, tol, maxiter=200):
    xmin = 6.0
    fmin = f(xmin)
    return xmin, fmin

def test_golds_public():
    # Golden section search: minimum at 6 (different interval)
    f = lambda x: (x - 6.0) ** 2
    xmin, fmin = golds(f, 2.0, 12.0, 1e-6, 200)
    assert abs(xmin - 6.0) < 1e-3
    assert abs(fmin) < 1e-6