import numpy as np
from normal_integration.core import horn_brooks

def test_basic_hb():
    p = np.zeros((5, 5))
    q = np.ones((5, 5))
    mask = np.ones((5, 5))
    z = horn_brooks(p, q, mask)
    assert z.shape == (5, 5)

def test_default_mask_hb():
    p = np.random.rand(2, 2)
    q = np.random.rand(2, 2)
    z = horn_brooks(p, q)
    assert z.shape == (2, 2)