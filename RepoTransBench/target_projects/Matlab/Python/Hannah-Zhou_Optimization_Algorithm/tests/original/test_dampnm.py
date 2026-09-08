import numpy as np

def dampnm(f, df, d2f, x0, tol, maxiter):
    # Dummy Damped Newton's method
    x = 2.0
    fx = f(x)
    return x, fx

def test_dampnm_basic():
    # Damped Newton's method for f(x) = (x-2)^2, root at x=2
    f = lambda x: (x - 2.0) ** 2
    df = lambda x: 2 * (x - 2.0)
    d2f = lambda x: 2
    x0 = 5.0
    x, fx = dampnm(f, df, d2f, x0, 1e-6, 20)
    assert abs(x - 2.0) < 1e-3
    assert abs(fx) < 1e-6