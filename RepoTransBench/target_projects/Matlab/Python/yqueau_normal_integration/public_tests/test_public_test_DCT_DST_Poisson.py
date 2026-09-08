import numpy as np
from normal_integration.core import DCT_Poisson, DST_Poisson

def test_dct_small_public():
    p = np.ones((2,2)) * 2
    q = np.ones((2,2))
    z = DCT_Poisson(p, q)
    assert z.shape == (2,2)

def test_dst_small_public():
    p = np.array([[4,2],[1,3]])
    q = np.array([[5,0],[0,5]])
    u_b = np.zeros((2,2))
    z = DST_Poisson(p, q, u_b)
    assert z.shape == (2,2)