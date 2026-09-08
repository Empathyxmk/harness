import numpy as np
from normal_integration.core import horn_brooks

def test_alternate_basic_hb():
    p = np.ones((4, 6))
    q = np.zeros((4, 6))
    mask = np.ones((4, 6))
    z = horn_brooks(p, q, mask)
    assert z.shape == (4, 6)

def test_smaller_default_mask_hb():
    p = np.random.rand(3,4)
    q = np.random.rand(3,4)
    z = horn_brooks(p, q)
    assert z.shape == (3,4)