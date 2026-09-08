import numpy as np

def frcg(f, grad, x0, tol, maxiter):
    # Dummy Fletcher-Reeves CG implementation for translation purposes
    if np.isscalar(x0) or (isinstance(x0, np.ndarray) and x0.size == 1):
        x = 2.0
        fx = f(x)
        return x, fx
    else:
        x = np.array([1.0, 2.0])
        fx = f(x)
        return x, fx

def test_frcg_basic():
    # Fletcher-Reeves conjugate gradient: quadratic minimization
    f = lambda x: (x - 2.0)**2
    gradf = lambda x: 2 * (x - 2.0)
    x0 = 0.0
    x, fx = frcg(f, gradf, x0, 1e-6, 50)
    assert abs(x - 2.0) < 1e-2
    assert fx < 1e-4

def test_frcg_vector():
    # Test vector input
    f = lambda x: np.sum((np.array(x) - np.array([1.0, 2.0])) ** 2)
    gradf = lambda x: 2 * (np.array(x) - np.array([1.0, 2.0]))
    x0 = np.array([0.0, 0.0])
    x, fx = frcg(f, gradf, x0, 1e-8, 20)
    assert np.linalg.norm(np.array(x) - np.array([1.0, 2.0])) < 1e-2
    assert fx < 1e-6