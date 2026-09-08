import numpy as np
from src.pidmd import tls

def test_tls_public():
    # PUBLIC: TLS test with different problem
    A = np.array([[2, 5], [0, 3], [4, 7]], dtype=float)
    b = np.array([9, 12, 17], dtype=float)
    x = tls(A, b)
    assert x.shape == (2, 1)
    x_ols = np.linalg.lstsq(A, b, rcond=None)[0]
    res_tls = np.linalg.norm(A @ x - b.reshape(-1, 1))
    res_ols = np.linalg.norm(A @ x_ols.reshape(-1,1) - b.reshape(-1, 1))
    assert res_tls <= res_ols * 1.1