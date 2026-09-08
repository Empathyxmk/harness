import numpy as np
from ukfmanifold.quaternions import isnormq, qnorm

def test_public_isnormq_col_and_row():
    Q = np.ones((4,1))
    Qn = qnorm(Q.T)
    assert isnormq(Q) == 1
    assert isnormq(Qn) == 2