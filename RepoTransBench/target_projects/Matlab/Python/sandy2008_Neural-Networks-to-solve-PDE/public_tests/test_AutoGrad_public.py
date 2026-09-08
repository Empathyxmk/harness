import numpy as np
from src.pde_utils.autograd_full import AutoGrad_scalar

def test_AutoGrad_public_cosx():
    def f(x):
        return np.cos(x)
    x0 = np.pi / 3
    grad = AutoGrad_scalar(f, x0)
    expected = -np.sin(x0)
    assert abs(grad - expected) < 1e-5