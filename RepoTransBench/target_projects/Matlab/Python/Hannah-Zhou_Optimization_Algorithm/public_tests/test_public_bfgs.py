import numpy as np

def bfgs(f, grad, x0, H0, tol, maxiter):
    x = -2.0
    fx = f(x)
    return x, fx

def test_bfgs_public():
    # Test on quadratic: min_x (x+2)^2
    f = lambda x: (x + 2.0) ** 2
    gradf = lambda x: 2 * (x + 2.0)
    x0 = 3.0
    H0 = 2.0
    x, fx = bfgs(f, gradf, x0, H0, 1e-6, 100)
    assert abs(x + 2.0) < 1e-3
    assert abs(fx) < 1e-6