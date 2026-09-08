import numpy as np
from normal_integration.core import mumford_shah_integration

def test_basic_ms():
    p = np.ones((4, 4))
    q = np.ones((4, 4))
    mask = np.ones((4, 4))
    z = mumford_shah_integration(p, q, mask)
    assert z.shape == (4, 4)
    assert np.all(np.isfinite(z))

def test_default_mask():
    p = np.random.rand(3, 3)
    q = np.random.rand(3, 3)
    z = mumford_shah_integration(p, q)
    assert z.shape == (3, 3)