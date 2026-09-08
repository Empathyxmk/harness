import numpy as np
from ukfmanifold.quaternions import qcvq

def test_qcvq_inverse_rotation():
    q = np.array([0.1, 0.2, 0.3, 0.9])
    v = np.array([1.5, 2.0, -3.1])
    # Should output vector rotated into "q's" frame
    res = qcvq(q, v)
    assert isinstance(res, np.ndarray)
    assert res.shape == (1,3)