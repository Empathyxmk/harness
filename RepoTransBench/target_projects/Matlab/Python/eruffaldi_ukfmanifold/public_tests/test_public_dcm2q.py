import numpy as np
from ukfmanifold.quaternions import dcm2q, q2dcm, qnorm

def test_public_dcm2q_roundtrip():
    q = np.array([0.5, 0.1, 0.2, 0.8])
    q = qnorm(q)
    R = q2dcm(q)
    q2 = dcm2q(R)
    assert np.allclose(np.abs(q), np.abs(q2), atol=1e-9)