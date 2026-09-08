import numpy as np
from lihongbo_consensus.helpers import normalization

def test_normalization_basic():
    v = np.array([2, 0])
    vn = normalization(v)
    assert abs(np.linalg.norm(vn) - 1) < 1e-10 or np.all(v == 0)

def test_normalization_zero():
    v0 = np.array([0, 0])
    vn0 = normalization(v0)
    assert np.all(vn0 == 0)