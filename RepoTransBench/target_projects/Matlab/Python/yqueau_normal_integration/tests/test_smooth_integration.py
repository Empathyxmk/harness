import numpy as np
from normal_integration.core import smooth_integration

def test_basic():
    p = np.zeros((4, 4))
    q = np.ones((4, 4))
    mask = np.ones((4, 4))
    z = smooth_integration(p, q, mask)
    assert z.shape == (4, 4)

def test_default_mask():
    p = np.random.rand(5, 5)
    q = np.random.rand(5, 5)
    z = smooth_integration(p, q)
    assert z.shape == (5, 5)

def test_edge_case():
    p = np.array([])
    q = np.array([])
    z = smooth_integration(p, q)
    assert z.size == 0