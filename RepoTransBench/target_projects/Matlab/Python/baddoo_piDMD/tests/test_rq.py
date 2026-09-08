import numpy as np
from src.pidmd import rq

def test_rq():
    # Test RQ factorization on a simple matrix
    A = np.array([[4, 3], [0, 5]], dtype=float)
    R1, Q1 = rq(A)
    assert np.linalg.norm(R1 @ Q1 - A, ord='fro') < 1e-10