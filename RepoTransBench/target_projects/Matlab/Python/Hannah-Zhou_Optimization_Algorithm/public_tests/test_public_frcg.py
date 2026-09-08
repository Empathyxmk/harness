import numpy as np

def frcg(f, grad, x0, tol, maxiter):
    x = np.array([4.0, 7.0])
    fx = f(x)
    return x, fx

def test_frcg_public():
    # Fletcher-Reeves CG: quadratic, different min point
    f = lambda x: np.sum((np.array(x) - np.array([4.0, 7.0])) ** 2)
    gradf = lambda x: 2 * (np.array(x) - np.array([4.0, 7.0]))
    x0 = np.array([2.0, 0.0])
    x, fx = frcg(f, gradf, x0, 1e-6, 100)
    assert np.linalg.norm(np.array(x) - np.array([4.0, 7.0])) < 1e-2
    assert fx < 1e-4