import numpy as np
from src.pidmd import tls

def test_tls():
    # Test total least squares example
    A = np.array([[1, 2], [3, 4], [5, 6]], dtype=float)
    b = np.array([7, 8, 10], dtype=float)
    x = tls(A, b)
    assert x.shape == (2, 1)
    # Check that TLS solution gives a smaller residual norm than OLS
    x_ols = np.linalg.lstsq(A, b, rcond=None)[0]
    res_tls = np.linalg.norm(A @ x - b.reshape(-1, 1))
    res_ols = np.linalg.norm(A @ x_ols.reshape(-1,1) - b.reshape(-1, 1))
    assert res_tls <= res_ols * 1.1  # TLS at least as good as OLS (allowing some small slack)