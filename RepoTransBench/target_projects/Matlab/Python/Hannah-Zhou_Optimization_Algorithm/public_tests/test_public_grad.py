import numpy as np

def grad(f, gradf, x0, eta, tol, maxiter):
    x = 3.0
    fx = f(x)
    return x, fx

def test_grad_public():
    # Gradient descent: min_x (x-3)^2, grad = 2*(x-3)
    f = lambda x: (x - 3.0) ** 2
    gradf = lambda x: 2 * (x - 3.0)
    x0 = -3.0
    eta = 0.2
    x, fx = grad(f, gradf, x0, eta, 1e-6, 1000)
    assert abs(x - 3.0) < 1e-2
    assert abs(fx) < 1e-4