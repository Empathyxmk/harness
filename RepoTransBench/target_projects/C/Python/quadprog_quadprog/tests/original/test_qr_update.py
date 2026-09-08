import numpy as np
import pytest

# Python implementations mirroring the C stub functions for testing householder
# reflector and its application, as defined in the original C test file.
# The C test file uses stubs for `householder_reflector` and `apply_householder`
# within the test itself, so we replicate that stub behavior here for consistency.

def householder_reflector_stub(n, x, v, beta, tau):
    """Mimics the C stub for householder_reflector."""
    beta[0] = 0.5
    tau[0] = 1.0
    for i in range(n):
        v[i] = x[i]

def apply_householder_stub(m, n, Q, v, beta_val, from_row):
    """Mimics the C stub for apply_householder (modifies Q in-place)."""
    # Fake application: scale matrix Q "somehow"
    # Q is assumed flattened, so Q[i*n] corresponds to Q[i][0]
    for i in range(from_row, m):
        Q[i*n] += beta_val * v[0]

def test_householder_reflector_basic():
    x = np.array([3.0, 4.0])
    v = np.zeros(2)
    beta = np.zeros(1) # Using array to pass by reference for a scalar
    tau = np.zeros(1)
    
    householder_reflector_stub(2, x, v, beta, tau)
    
    np.testing.assert_allclose(v, [3.0, 4.0], atol=1e-9)
    np.testing.assert_allclose(beta[0], 0.5, atol=1e-9)
    np.testing.assert_allclose(tau[0], 1.0, atol=1e-9)

def test_apply_householder_basic():
    Q = np.array([1., 2., 3., 4., 5., 6.]) # Flattened 2x3 matrix
    v = np.array([7., 8.])
    beta_val = 0.5
    
    apply_householder_stub(2, 3, Q, v, beta_val, 0)
    
    # Expected values based on the C stub: Q[0] += 0.5*7, Q[3] += 0.5*7
    expected_Q_0 = 1.0 + 0.5 * 7
    expected_Q_3 = 4.0 + 0.5 * 7
    
    np.testing.assert_allclose(Q[0], expected_Q_0, atol=1e-9)
    np.testing.assert_allclose(Q[3], expected_Q_3, atol=1e-9)