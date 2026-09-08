import numpy as np
from ukfmanifold.quaternions import qconj, qmult, qnorm

def test_self_conj():
    q = np.array([0.2, 0.4, 0.3, 0.7])
    q = qnorm(q)
    qc = qconj(q)
    out = qmult(q, qc)
    # Norm squared quaternion, so product should be identity [0 0 0 1]
    assert np.allclose(out, np.array([0,0,0,1]), atol=1e-10)