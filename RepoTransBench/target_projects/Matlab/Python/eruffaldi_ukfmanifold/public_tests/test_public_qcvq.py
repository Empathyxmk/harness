import numpy as np
from ukfmanifold.quaternions import qcvq

def test_public_qcvq_dim():
    q = np.array([0.1, 0.2, 0.3, 0.9])
    v = np.array([1.0, 2.0, 3.0])
    out = qcvq(q, v)
    assert out.shape == (1,3)