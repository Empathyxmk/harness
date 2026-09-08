import numpy as np
from normal_integration.core import phi1_integration, phi2_integration

def test_phi1_integration_public():
    p = np.array([[2, 3], [5, 7]])
    q = np.ones((2,2))
    mask = np.array([[1,1],[0,0]])
    lambda_ = np.ones((2,2)) * 0.02
    zinit = np.zeros((2,2))
    z = phi1_integration(p, q, mask, lambda_, zinit, 0.2, 15, 1e-4, zinit)
    assert z.shape == (2,2)

def test_phi2_integration_public():
    p = np.array([[4,2],[8,6]])
    q = np.array([[1,3],[5,7]])
    mask = np.array([[1,0],[1,0]])
    lambda_ = np.ones((2,2)) * 0.02
    zinit = np.zeros((2,2))
    z = phi2_integration(p, q, mask, lambda_, zinit, 0.2, 12, 1e-4, zinit)
    assert z.shape == (2,2)