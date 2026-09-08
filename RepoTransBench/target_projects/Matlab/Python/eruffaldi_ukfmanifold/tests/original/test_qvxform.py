import numpy as np
from ukfmanifold.quaternions import qvxform, qnorm

def test_qvxform_rotate_identity():
    # Rotating by identity quaternion should leave vector unchanged
    q = np.array([0,0,0,1])
    v = np.array([1.0, 2.0, -1.0])
    w = qvxform(q, v)
    assert np.allclose(w, v, atol=1e-10)