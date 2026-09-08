import numpy as np
from ukfmanifold.quaternions import qdecomp, qnorm

def test_public_qdecomp_rotation_identity():
    # Identity quaternion: axis arbitrary, angle zero
    q = np.array([0,0,0,1])
    phi, n = qdecomp(q)
    assert np.isclose(phi, 0, atol=1e-14)
    assert np.allclose(n, np.zeros_like(n))