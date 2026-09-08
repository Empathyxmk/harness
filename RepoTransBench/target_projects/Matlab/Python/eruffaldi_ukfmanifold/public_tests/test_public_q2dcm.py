import numpy as np
from ukfmanifold.quaternions import q2dcm, qnorm

def test_public_q2dcm_match_expected():
    Q = np.array([
        [0, 0, 0, 1],
        [0, 0, 1, 0]
    ], dtype=float)
    Q = qnorm(Q)
    v = np.array([1,0,0])
    A = q2dcm(Q)
    assert A.shape == (3,3,2)
    res0 = A[:,:,0]@v
    res1 = A[:,:,1]@v
    assert np.allclose(res0, [1,0,0])
    assert np.allclose(res1, [1,0,0])