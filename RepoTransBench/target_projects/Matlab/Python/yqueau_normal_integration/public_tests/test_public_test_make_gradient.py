import numpy as np
from normal_integration.core import make_gradient

def test_gradient_diff_data_public():
    z = np.array([[0,0,0],[1,3,5]])
    p, q = make_gradient(z)
    assert p.shape == z.shape
    assert q.shape == z.shape