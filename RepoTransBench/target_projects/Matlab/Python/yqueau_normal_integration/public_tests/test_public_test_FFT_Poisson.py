import numpy as np
from normal_integration.core import FFT_Poisson

def test_diff_small_system():
    f = np.ones((3, 5)) * 2
    sol = FFT_Poisson(f)
    assert sol.shape == f.shape
    assert np.all(np.isfinite(sol))

def test_diff_nonzero_boundary():
    f = np.array([[4,3], [2,1]])
    z0 = np.array([[1,2],[3,4]])
    sol = FFT_Poisson(f, z0)
    assert sol.shape == f.shape