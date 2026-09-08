import numpy as np
from ukfmanifold.quaternions import qvqc, qnorm

def test_public_qvqc_vector_rot():
    q = np.array([0.2, 0.0, 0.0, 0.98])
    v = np.array([1.0, 0.0, 0.0])
    q = qnorm(q)
    w = qvqc(q, v)
    assert w.shape == (3,)