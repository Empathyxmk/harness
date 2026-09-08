import numpy as np
from normal_integration.core import DCT_Poisson, DST_Poisson

def test_DCT_Poisson():
    f = np.ones((5, 5))
    sol = DCT_Poisson(f)
    assert sol.shape == f.shape
    assert np.all(np.isfinite(sol))

def test_DST_Poisson():
    f = np.random.rand(6, 6)
    sol = DST_Poisson(f)
    assert sol.shape == f.shape
    assert np.all(~np.isnan(sol))