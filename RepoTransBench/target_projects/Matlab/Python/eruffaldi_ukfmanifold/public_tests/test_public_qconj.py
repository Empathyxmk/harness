import numpy as np
from ukfmanifold.quaternions import qconj, qnorm, qmult

def test_public_qconj_inverse_rotation():
    q = np.array([0,0,1,0])
    q = qnorm(q)
    qc = qconj(q)
    prod = qmult(q, qc)
    assert np.allclose(prod, [0,0,0,1], atol=1e-10)