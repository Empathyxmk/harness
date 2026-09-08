import numpy as np
from normal_integration.core import smooth_integration

def test_smooth_diff_shape_public():
    p = np.array([[1,2,1],[2,1,2]])
    q = np.array([[0,0,1],[1,0,2]])
    mask = np.ones((2,3))
    lambda_ = np.ones((2,3)) * 1e-3
    z0 = np.zeros((2,3))
    z = smooth_integration(p, q, mask, lambda_, z0, 'pcg', 'none')
    assert z.shape == (2,3)