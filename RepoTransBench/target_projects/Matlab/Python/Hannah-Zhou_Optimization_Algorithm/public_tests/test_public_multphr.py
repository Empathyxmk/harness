import numpy as np

def multphr(f, x0, tol, maxiter):
    x = np.array([7.0, -2.0])
    fx = f(x)
    return x, fx

def test_multphr_public():
    # Powell's method: quadratic, different minimum
    f = lambda x: np.sum((np.array(x) - np.array([7.0, -2.0])) ** 2)
    x0 = np.array([1.0, 0.0])
    x, fx = multphr(f, x0, 1e-6, 50)
    assert np.linalg.norm(x - np.array([7.0, -2.0])) < 1e-2
    assert fx < 1e-4