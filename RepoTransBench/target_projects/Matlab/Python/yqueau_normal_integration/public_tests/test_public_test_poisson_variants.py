import numpy as np
from normal_integration.core import FFT_Poisson, DCT_Poisson, DST_Poisson

def test_fft_poisson_ones_public():
    f = np.ones((3,5)) * 3
    sol = FFT_Poisson(f)
    assert sol.shape == f.shape

def test_dct_poisson_diff_public():
    f = np.array([[7,3],[5,9]])
    sol = DCT_Poisson(f)
    assert sol.shape == f.shape

def test_dst_poisson_diff_public():
    f = np.array([[1,1,2],[0,3,4]])
    sol = DST_Poisson(f)
    assert sol.shape == f.shape