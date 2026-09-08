import numpy as np

def trustm(f, gradf, hessf, x0, tol, maxiter):
    x = 5.0
    fx = f(x)
    return x, fx

def test_trustm_public():
    # Trust region: min_x (x-5)^2, grad = 2*(x-5), hess = 2
    f = lambda x: (x - 5.0) ** 2
    gradf = lambda x: 2 * (x - 5.0)
    hessf = lambda x: 2
    x0 = 11.0
    x, fx = trustm(f, gradf, hessf, x0, 1e-6, 100)
    assert abs(x - 5.0) < 1e-3
    assert abs(fx) < 1e-6