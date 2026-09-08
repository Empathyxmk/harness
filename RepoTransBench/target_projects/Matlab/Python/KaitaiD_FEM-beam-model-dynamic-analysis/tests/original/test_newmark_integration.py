import numpy as np
import pytest
from src.fem.newmark import newmark_int

def test_newmark_integration_shapes_and_nan():
    # Use a simple SDOF system parameters
    M = 2.0
    K = 16.0
    C = 0.8
    dt = 0.05
    nt = 5
    F = np.ones((nt+1,))
    U0 = 0
    V0 = 0

    U, V, A = newmark_int(M, K, C, F, U0, V0, dt, nt)

    assert U.shape == (nt+1, 1)
    assert V.shape == (nt+1, 1)
    assert A.shape == (nt+1, 1)
    assert not np.isnan(U).any()
    assert not np.isnan(V).any()
    assert not np.isnan(A).any()