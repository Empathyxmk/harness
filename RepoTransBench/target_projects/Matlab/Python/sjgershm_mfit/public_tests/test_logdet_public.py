import pytest
import numpy as np
from src.logdet import logdet

def test_2x2_sym_pd():
    A = np.array([[3,2],[2,6]])
    val1 = logdet(A)
    val2 = np.log(np.linalg.det(A))
    assert np.allclose(val1, val2, atol=1e-10)

def test_3x3_sym_pd_chol():
    np.random.seed(42)
    A = np.random.rand(3,3)
    C = A @ A.T
    v1 = logdet(C, 'chol')
    v2 = np.log(np.linalg.det(C))
    assert np.allclose(v1, v2, atol=1e-10)

def test_non_sym_matrix():
    A = np.array([[2,1],[0,2]])
    v1 = logdet(A)
    v2 = np.log(np.linalg.det(A))
    assert np.allclose(v1, v2, atol=1e-10)

def test_negative_determinant_public():
    A = np.array([[-1,0],[0,-5]])
    val = logdet(A)
    expected = np.log(np.abs(np.linalg.det(A)))
    assert np.allclose(val, expected, atol=1e-10)

def test_invalid_arg_error_public():
    A = np.array([[3+3j,1],[0,2]])
    with pytest.raises(ValueError, match="logdet:invalidarg"):
        logdet(A)