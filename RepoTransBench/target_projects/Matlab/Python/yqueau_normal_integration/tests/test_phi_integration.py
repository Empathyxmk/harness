import numpy as np
from normal_integration.core import phi1_integration, phi2_integration

def test_phi1_basic():
    p = np.eye(3)
    q = np.eye(3)
    mask = np.ones((3, 3))
    z = phi1_integration(p, q, mask)
    assert z.shape == (3, 3)

def test_phi2_basic():
    p = np.random.rand(4, 4)
    q = np.random.rand(4, 4)
    mask = np.ones((4, 4))
    z = phi2_integration(p, q, mask)
    assert z.shape == (4, 4)