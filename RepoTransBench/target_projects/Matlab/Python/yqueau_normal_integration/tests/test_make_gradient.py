import numpy as np
from normal_integration.core import make_gradient

def test_basic_gradient():
    z = np.array([[1, 2], [3, 4]])
    p, q = make_gradient(z)
    assert p.shape == z.shape
    assert q.shape == z.shape

def test_gradient_with_mask():
    z = np.array([[1, 2, 3], [4, 5, 6]])
    mask = np.array([[1, 0, 1], [1, 1, 1]], dtype=bool)
    p, q = make_gradient(z, mask)
    assert p.shape == z.shape
    assert q.shape == z.shape
    assert np.all(p[~mask] == 0)
    assert np.all(q[~mask] == 0)

def test_gradient_vector_input():
    z = np.arange(1, 7)
    p, q = make_gradient(z)
    assert p.ndim == 1 or p.size == 1
    assert q.ndim == 1 or q.size == 1