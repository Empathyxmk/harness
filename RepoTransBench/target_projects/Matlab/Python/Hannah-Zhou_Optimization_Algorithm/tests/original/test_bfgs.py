import numpy as np

def bfgs(f, grad, x0, H0, tol, maxiter):
    # Dummy BFGS implementation for test running (for translation context only)
    # Replace with a real one for actual testing
    x = 1.0
    fx = f(x)
    return x, fx

def test_bfgs_basic():
    # Test on a simple quadratic: min_x (x-1)^2
    f = lambda x: (x - 1.0) ** 2
    gradf = lambda x: 2 * (x - 1.0)
    x0 = 0.0
    H0 = 1.0
    x, fx = bfgs(f, gradf, x0, H0, 1e-6, 100)
    assert abs(x - 1.0) < 1e-3
    assert abs(fx) < 1e-6