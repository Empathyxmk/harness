import numpy as np
import pytest
from src.fem.newmark import newmark_int

def test_newmark_integration_public_shapes_and_nan():
    # Different inputs for public test
    M = 4.0
    K = 25.0
    C = 1.0
    dt = 0.02
    nt = 7
    F = 2 * np.ones((nt+1,))
    U0 = 1
    V0 = -0.2

    U, V, A = newmark_int(M, K, C, F, U0, V0, dt, nt)

    assert U.shape == (nt+1, 1)
    assert V.shape == (nt+1, 1)
    assert A.shape == (nt+1, 1)
    assert not np.isnan(U).any()
    assert not np.isnan(V).any()
    assert not np.isnan(A).any()