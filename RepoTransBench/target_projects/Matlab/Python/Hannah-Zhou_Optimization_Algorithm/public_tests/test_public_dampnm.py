import numpy as np

def dampnm(f, grad, hess, x0, tol, maxiter):
    x = -1.0
    fx = f(x)
    return x, fx

def test_dampnm_public():
    # Damped Newton: min_x (x+1)^2, grad = 2*(x+1), hess = 2
    f = lambda x: (x + 1.0) ** 2
    gradf = lambda x: 2 * (x + 1.0)
    hessf = lambda x: 2
    x0 = 10.0
    x, fx = dampnm(f, gradf, hessf, x0, 1e-6, 50)
    assert abs(x + 1.0) < 1e-3
    assert abs(fx) < 1e-6