import numpy as np
from ukfmanifold.quaternions import qvqc, qnorm

def test_qvqc_rotation_inverse():
    q = np.array([0.1, 0.2, 0.3, 0.9])
    v = np.array([0.0, 1.0, 0.0])
    q = qnorm(q)
    w = qvqc(q, v)
    assert w.shape == (3,)
    # Should produce a rotated vector