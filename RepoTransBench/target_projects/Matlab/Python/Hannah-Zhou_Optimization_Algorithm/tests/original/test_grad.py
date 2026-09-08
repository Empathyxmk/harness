import numpy as np

def grad(f, x):
    # Approximate gradient for scalar or vector input
    x = np.array(x, dtype=float)
    h = 1e-8
    if np.isscalar(x) or x.shape == ():
        return (f(x + h) - f(x - h)) / (2 * h)
    g = np.zeros_like(x)
    for i in range(len(x)):
        xp = x.copy()
        xm = x.copy()
        xp[i] += h
        xm[i] -= h
        g[i] = (f(xp) - f(xm)) / (2 * h)
    return g

def test_grad_scalar():
    f = lambda x: (x - 2.0)**2
    g = grad(f, 2.0)
    assert abs(g) < 1e-4

def test_grad_vector():
    f = lambda x: np.sum((np.array(x) - np.array([1.0, 3.0])) ** 2)
    g = grad(f, np.array([1.0, 3.0]))
    assert np.all(np.abs(g) < 1e-4)