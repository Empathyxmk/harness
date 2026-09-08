import numpy as np
from ukfmanifold.quaternions import qnorm

def test_public_unit_norms_many():
    Q = np.random.randn(30,4)
    Qn = qnorm(Q)
    for i in range(30):
        assert np.isclose(np.linalg.norm(Qn[i]), 1.0, rtol=1e-10)