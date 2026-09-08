import pytest
import numpy as np

# These would be your real implementations:
def learn(alpha, b, x, y, K, Q, k, l, I, J):
    # Fake minimal mock for demonstration. Replace with real implementation.
    if (I is None or len(I) == 0) or (J is None or len(J) == 0):
        return alpha.copy(), b, True
    # Just do a dummy update for test purposes:
    alpha_new = alpha.copy()
    alpha_new[I[0]-1 if hasattr(I[0],'__index__') else I[0]] += 1.0
    b_new = b + 0.5
    converged_flag = False
    return alpha_new, b_new, converged_flag

def test_case1_basic_learning_step():
    # Define a simple linear kernel function for testing (used to compute K and Q)
    def k_func(xi, xj):
        return np.dot(xi, xj)

    x = np.array([[0, 0], [1, 1]])
    y = np.array([1, -1])
    K = np.array([
        [k_func(x[0], x[0]), k_func(x[0], x[1])],
        [k_func(x[1], x[0]), k_func(x[1], x[1])]
    ])
    Q = K * np.outer(y, y)
    alpha = np.zeros((x.shape[0],))
    b = 0
    k = np.zeros_like(y, dtype=float)
    l = np.zeros_like(y, dtype=float)
    I = [1]
    J = [2]
    alpha_new, b_new, converged_flag = learn(alpha, b, x, y, K, Q, k, l, I, J)
    assert alpha_new.shape == (2,)
    assert np.isscalar(b_new)
    assert isinstance(converged_flag, (bool, np.bool_))
    assert np.any(alpha_new != 0) or b_new != 0

def test_case2_empty_I_or_J():
    def k_func(xi, xj):
        return np.dot(xi, xj)
    x = np.array([[0, 0], [1, 1]])
    y = np.array([1, -1])
    K = np.array([
        [k_func(x[0], x[0]), k_func(x[0], x[1])],
        [k_func(x[1], x[0]), k_func(x[1], x[1])]
    ])
    Q = K * np.outer(y, y)
    alpha = np.zeros((x.shape[0],))
    b = 0
    k = np.zeros_like(y, dtype=float)
    l = np.zeros_like(y, dtype=float)

    I = []
    J = [1]
    _, _, converged_flag = learn(alpha, b, x, y, K, Q, k, l, I, J)
    assert converged_flag is True

    I = [1]
    J = []
    _, _, converged_flag = learn(alpha, b, x, y, K, Q, k, l, I, J)
    assert converged_flag is True

def test_case3_I_eq_J_branch():
    x = np.array([[0,0],[1,1],[0,1]])
    y = np.array([1, -1, 1])
    K = x @ x.T
    Q = K * np.outer(y, y)
    alpha = np.zeros((x.shape[0],))
    b = 0
    k = np.zeros_like(y, dtype=float)
    l = np.zeros_like(y, dtype=float)
    I = [1]
    J = [1]
    alpha_new, b_new, converged_flag = learn(alpha, b, x, y, K, Q, k, l, I, J)
    assert alpha_new.shape == (3,)
    assert np.isscalar(b_new)
    assert isinstance(converged_flag, (bool, np.bool_))

def test_case4_large_data():
    np.random.seed(42)
    x = np.vstack([np.random.randn(10,2)+2, np.random.randn(10,2)-2])
    y = np.concatenate([np.ones(10), -np.ones(10)])
    K = x @ x.T
    Q = K * np.outer(y,y)
    alpha = np.zeros((x.shape[0],))
    b = 0
    k = np.zeros_like(y, dtype=float)
    l = np.zeros_like(y, dtype=float)
    I = [1]
    J = [2]
    alpha_new, b_new, converged_flag = learn(alpha, b, x, y, K, Q, k, l, I, J)
    assert alpha_new.shape == (20,)
    assert np.isscalar(b_new)