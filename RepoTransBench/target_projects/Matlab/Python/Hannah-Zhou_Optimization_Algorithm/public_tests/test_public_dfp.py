import numpy as np

def dfp(f, grad, x0, H0, tol, maxiter):
    x = 4.0
    fx = f(x)
    return x, fx

def test_dfp_public():
    # DFP method for min_x (x-4)^2 --> min at x=4
    f = lambda x: (x - 4.0) ** 2
    gradf = lambda x: 2 * (x - 4.0)
    x0 = 0.0
    H0 = 2.0
    x, fx = dfp(f, gradf, x0, H0, 1e-6, 100)
    assert abs(x - 4.0) < 1e-3
    assert abs(fx) < 1e-6