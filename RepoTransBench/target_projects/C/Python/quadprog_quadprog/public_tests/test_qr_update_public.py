import numpy as np
import pytest

# Python implementations mirroring the C linear algebra functions for QR updates.

def qr_decompose(A_flat, Q_out, R_out, m, n):
    """Mimics C's qr_decompose, returning Q and R."""
    A_mat = np.array(A_flat).reshape((m, n))
    Q_np, R_np = np.linalg.qr(A_mat)
    
    # Flatten and copy to output arrays, as C expects
    Q_out[:] = Q_np.flatten()
    R_out[:] = R_np.flatten()

def mat_mult(A_flat, B_flat, C_out, m, k, n):
    """Mimics C's mat_mult (C = A @ B)."""
    A_mat = np.array(A_flat).reshape((m, k))
    B_mat = np.array(B_flat).reshape((k, n))
    C_np = A_mat @ B_mat
    C_out[:] = C_np.flatten()

def mat_mult_transposeA(A_flat, B_flat, C_out, m, k, n):
    """Mimics C's mat_mult_transposeA (C = A.T @ B)."""
    A_mat = np.array(A_flat).reshape((m, k))
    B_mat = np.array(B_flat).reshape((m, n)) # Assuming B is m x n for A.T @ B
    C_np = A_mat.T @ B_mat
    C_out[:] = C_np.flatten()

def test_qr_decompose_public():
    A = np.array([1.0, 2.0, 2.0, 1.5]) # Flattened 2x2 matrix
    Q = np.zeros(4)
    R = np.zeros(4)
    qr_decompose(A, Q, R, 2, 2)

    Q_mat = Q.reshape((2, 2))
    R_mat = R.reshape((2, 2))
    A_mat = A.reshape((2,2))

    # check Q*R = A
    QR_mat = Q_mat @ R_mat
    np.testing.assert_allclose(QR_mat, A_mat, atol=1e-5)

    # check Q is orthogonal: Q'*Q = I
    QQ_mat = Q_mat.T @ Q_mat
    np.testing.assert_allclose(QQ_mat, np.eye(2), atol=1e-5)