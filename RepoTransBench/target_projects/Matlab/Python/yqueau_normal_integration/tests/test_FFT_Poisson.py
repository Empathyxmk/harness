import numpy as np
from normal_integration.core import FFT_Poisson

def test_small_system():
    f = np.ones((4, 4))
    sol = FFT_Poisson(f)
    assert sol.shape == f.shape
    assert np.all(np.isfinite(sol))

def test_nonzero_boundary():
    f = np.array([[1, 2], [3, 4]])
    z0 = np.zeros((2, 2))
    sol = FFT_Poisson(f, z0)
    assert sol.shape == f.shape