import numpy as np
from normal_integration.core import mumford_shah_integration

def test_ms_single_mask_val_public():
    p = np.ones((2,3)) * 3
    q = np.zeros((2,3))
    mask = np.array([[1,1,0],[0,1,1]])
    lambda_ = np.ones((2,3)) * 0.05
    z0 = np.zeros((2,3))
    z = mumford_shah_integration(p, q, mask, lambda_, z0, 0.11, 17, 1e-4, z0, 0.4)
    assert z.shape == (2,3)