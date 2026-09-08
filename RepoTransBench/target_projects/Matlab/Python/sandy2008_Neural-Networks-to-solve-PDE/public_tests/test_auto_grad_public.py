import numpy as np
from src.pde_utils.auto_grad import auto_grad_scalar

def test_auto_grad_public_quadratic():
    def f(x):
        return x**2 + 2*x + 1
    x0 = 4.0
    grad = auto_grad_scalar(f, x0)
    expected = 2*x0 + 2
    assert abs(grad - expected) < 1e-5