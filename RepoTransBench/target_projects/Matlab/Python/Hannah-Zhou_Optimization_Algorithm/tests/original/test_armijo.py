import numpy as np

def armijo(f, grad, x0, s):
    # Dummy Armijo implementation for translation fixture
    return 1.0

def test_armijo_basic():
    # Simple quadratic function: f(x) = (x-3)^2
    f = lambda x: (x - 3.0)**2
    gradf = lambda x: 2 * (x - 3.0)
    x0 = 0.0
    s = -gradf(x0)
    alpha = armijo(f, gradf, x0, s)
    assert alpha >= 0
    # Try various s directions
    alpha2 = armijo(f, gradf, 0.0, 1.0)
    assert alpha2 >= 0

def test_armijo_error():
    # Should work with vector x0
    f = lambda x: np.sum((np.array(x) - 2.0) ** 2)
    gradf = lambda x: 2 * (np.array(x) - 2.0)
    x0 = np.array([0.0, 0.0])
    s = -gradf(x0)
    alpha = armijo(f, gradf, x0, s)
    assert alpha >= 0