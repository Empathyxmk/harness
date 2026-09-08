import numpy as np

def armijo(f, grad, x0, p, dummy=1):
    # Dummy Armijo public version for test translation
    alpha = 1.0
    phi_a = f(x0 + alpha * p)
    phip_a = None
    return alpha, phi_a, phip_a

def test_armijo_public():
    # Armijo rule line search: f(x) = (x-8)^2, grad = 2*(x-8)
    f = lambda x: (x - 8.0) ** 2
    gradf = lambda x: 2 * (x - 8.0)
    x0 = 2.0
    p = 1.0
    alpha, phi_a, phip_a = armijo(f, gradf, x0, p, 1)
    assert alpha > 0
    assert phi_a < f(x0)