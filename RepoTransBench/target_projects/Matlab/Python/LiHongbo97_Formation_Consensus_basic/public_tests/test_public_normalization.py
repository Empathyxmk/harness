import numpy as np
from lihongbo_consensus.helpers import normalization

def test_public_normalization_diff_vector():
    v = np.array([0, 5])
    vn = normalization(v)
    assert abs(np.linalg.norm(vn) - 1) < 1e-10 or np.all(v == 0)

def test_public_normalization_zero_vector():
    v0 = np.array([0, 0])
    vn0 = normalization(v0)
    assert np.all(vn0 == 0)