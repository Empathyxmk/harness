import numpy as np
from normal_integration.core import tv_integration

def test_basic_tv():
    p = np.ones((3, 3))
    q = np.ones((3, 3))
    mask = np.ones((3, 3))
    z = tv_integration(p, q, mask)
    assert z.shape == (3, 3)

def test_default_args():
    p = np.ones((3, 3))
    q = np.zeros((3, 3))
    z = tv_integration(p, q)
    assert z.shape == (3, 3)