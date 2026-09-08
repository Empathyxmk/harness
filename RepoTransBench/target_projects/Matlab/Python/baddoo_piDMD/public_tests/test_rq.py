import numpy as np
from src.pidmd import rq

def test_rq_public():
    # PUBLIC: RQ test with a different matrix
    A = np.array([[7, 1], [3, 8]], dtype=float)
    R1, Q1 = rq(A)
    assert np.linalg.norm(R1 @ Q1 - A, ord='fro') < 1e-10