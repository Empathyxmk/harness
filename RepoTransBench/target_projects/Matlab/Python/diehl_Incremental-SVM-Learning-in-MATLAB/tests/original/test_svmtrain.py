import numpy as np
import pytest

# This should be replaced with the real SVM train implementation.
def svmtrain(x, y, C=None, tol=None):
    # Dummy stub: returns alphas, bias, K, Q, x_sv, y_sv, sv_idx
    n = x.shape[0]
    alpha = np.ones(n, dtype=x.dtype)
    b = np.float32(0.42) if x.dtype == np.float32 else 0.42
    K = x @ x.T
    Q = K * np.outer(y, y)
    sv_idx = np.arange(n)
    x_sv = x[sv_idx]
    y_sv = y[sv_idx]
    return alpha, b, K, Q, x_sv, y_sv, sv_idx

def test_basic_linear_data():
    x = np.array([[-1, -1], [1,1], [-1,1], [1,-1]])
    y = np.array([-1, -1, 1, 1])
    alpha, b, K, Q, x_sv, y_sv, sv_idx = svmtrain(x, y)
    assert len(alpha) == x.shape[0]
    assert np.isscalar(b)
    assert len(sv_idx) > 0
    assert x_sv.shape[0] == len(sv_idx)
    assert y_sv.shape[0] == len(sv_idx)
    # Single precision check
    x_single = x.astype(np.float32)
    y_single = y.astype(np.float32)
    alpha_s, b_s, K_s, Q_s, x_sv_s, y_sv_s, sv_idx_s = svmtrain(x_single, y_single)
    assert alpha_s.dtype == np.float32

def test_with_c_param():
    x = np.array([[0,0],[1,1],[0,1],[1,0]])
    y = np.array([1,1,-1,-1])
    C = 10
    alpha, b, K, Q, x_sv, y_sv, sv_idx = svmtrain(x, y, C)
    assert len(alpha) == x.shape[0]
    assert np.isscalar(b)
    assert len(sv_idx) > 0

def test_more_complex_data():
    np.random.seed(123)
    x = np.vstack([np.random.randn(50,2)+2, np.random.randn(50,2)-2])
    y = np.concatenate([np.ones(50), -np.ones(50)])
    alpha, b, K, Q, x_sv, y_sv, sv_idx = svmtrain(x, y)
    assert len(alpha) == x.shape[0]
    assert np.isscalar(b)
    assert len(sv_idx) > 0

def test_perfectly_separable_simple():
    x = np.array([[0,0],[1,1]])
    y = np.array([1,-1])
    alpha, b, K, Q, x_sv, y_sv, sv_idx = svmtrain(x, y)
    assert alpha is not None and b is not None