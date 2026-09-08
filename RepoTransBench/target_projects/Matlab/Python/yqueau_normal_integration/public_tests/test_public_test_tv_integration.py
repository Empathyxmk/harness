import numpy as np
from normal_integration.core import tv_integration

def test_tv_small_public():
    p = np.array([[1,2],[0,0]])
    q = np.array([[0,0],[2,1]])
    mask = np.ones((2,2))
    lambda_ = np.ones((2,2)) * 2
    z0 = np.zeros((2,2))
    zinit = np.array([[1,1],[2,2]])
    z = tv_integration(p, q, mask, lambda_, z0, 0.3, 20, 1e-4, zinit)
    assert z.shape == (2,2)

def test_tv_masked_public():
    p = np.array([[3,3,0],[1,1,2]])
    q = np.array([[2,0,0],[1,4,0]])
    mask = np.array([[1,0,1],[1,0,1]])
    lambda_ = np.ones((2,3)) * 0.2
    z0 = np.zeros((2,3))
    zinit = np.zeros((2,3))
    z = tv_integration(p, q, mask, lambda_, z0, 0.15, 10, 1e-4, zinit)
    assert z.shape == (2,3)