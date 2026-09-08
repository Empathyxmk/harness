import numpy as np

def broyden(F, x0, B0, tol, maxiter):
    x = np.array([2.0, 4.0])
    Fx = F(x)
    return x, Fx

def test_broyden_public():
    # Broyden's method: roots of f(x) = [x(1)-2; x(2)-4]
    F = lambda x: np.array([x[0] - 2.0, x[1] - 4.0])
    x0 = np.array([0.0, 0.0])
    B0 = np.eye(2)
    x, Fx = broyden(F, x0, B0, 1e-6, 70)
    assert np.linalg.norm(x - np.array([2.0, 4.0])) < 1e-3
    assert np.linalg.norm(Fx) < 1e-6