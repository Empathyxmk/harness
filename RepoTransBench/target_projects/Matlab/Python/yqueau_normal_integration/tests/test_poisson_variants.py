import numpy as np
from normal_integration.core import DCT_Poisson, DST_Poisson, FFT_Poisson

def test_DCT_Poisson_identity():
    g = np.eye(5)
    result = DCT_Poisson(g)
    assert result.shape == g.shape

def test_DST_Poisson_random():
    g = np.random.rand(4, 3)
    result = DST_Poisson(g)
    assert result.shape == g.shape
    assert np.all(np.isfinite(result))

def test_FFT_Poisson_zeros():
    g = np.zeros((6, 6))
    result = FFT_Poisson(g)
    assert result.shape == (6, 6)
    assert np.all(result == 0)