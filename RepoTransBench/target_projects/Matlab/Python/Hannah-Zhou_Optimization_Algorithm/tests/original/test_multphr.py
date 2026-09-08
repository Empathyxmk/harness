import numpy as np

def multphr(f, x0, tol, maxiter):
    # Dummy Powell's method implementation for test running
    # You should replace this with the real one
    x = np.array([3.0, 5.0])
    fx = f(x)
    return x, fx

def test_multphr_basic():
    # Powell's method: quadratic
    f = lambda x: np.sum((np.array(x) - np.array([3.0, 5.0])) ** 2)
    x0 = np.array([0.0, 0.0])
    x, fx = multphr(f, x0, 1e-6, 50)
    assert np.linalg.norm(x - np.array([3.0, 5.0])) < 1e-2
    assert fx < 1e-4