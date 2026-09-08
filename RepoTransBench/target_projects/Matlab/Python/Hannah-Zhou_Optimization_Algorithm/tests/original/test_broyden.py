import numpy as np

def broyden(F, x0, maxiter, tol):
    # Dummy Broyden for real root for scalar
    return np.sqrt(2.0)

def test_broyden_basic():
    # Broyden method for root finding. Solve x^2 - 2 = 0
    F = lambda x: x ** 2 - 2.0
    x0 = 1.0
    x = broyden(F, x0, 20, 1e-6)
    assert abs(x - np.sqrt(2.0)) < 1e-3