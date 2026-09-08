import numpy as np
from ukfmanifold.quaternions import qmult

def test_public_qmult_identity():
    q = np.array([0.2, 0.1, 0.1, 0.97])
    I = np.array([0,0,0,1])
    assert np.allclose(qmult(q, I), q)
    assert np.allclose(qmult(I, q), q)