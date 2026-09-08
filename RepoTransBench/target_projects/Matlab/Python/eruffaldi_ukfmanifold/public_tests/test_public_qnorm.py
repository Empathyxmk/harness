import numpy as np
from ukfmanifold.quaternions import qnorm

def test_public_qnorm_output():
    q = np.random.randn(4)
    qn = qnorm(q)
    normed = np.linalg.norm(qn)
    assert np.isclose(normed, 1.0, atol=1e-10)