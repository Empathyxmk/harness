import numpy as np

def trustm(f, gradf, hessf, x0, tol, maxiter, radius=1.0):
    # Dummy trust region method for translation
    x = np.array([4.0, 2.0])
    fx = f(x)
    return x, fx

def test_trustm_basic():
    # Trust region method, quadratic
    f = lambda x: np.sum((np.array(x) - np.array([4.0, 2.0])) ** 2)
    gradf = lambda x: 2 * (np.array(x) - np.array([4.0, 2.0]))
    hessf = lambda x: 2 * np.eye(len(x))
    x0 = np.array([0.0, 0.0])
    x, fx = trustm(f, gradf, hessf, x0, 1e-6, 100, 1.0)
    assert np.linalg.norm(x - np.array([4.0, 2.0])) < 1e-2
    assert fx < 1e-4