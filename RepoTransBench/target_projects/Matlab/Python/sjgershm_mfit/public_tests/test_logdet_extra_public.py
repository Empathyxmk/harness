import pytest
import numpy as np
from src.logdet import logdet

def test_larger_random_positive_definite():
    np.random.seed(123)
    A = np.random.rand(6,6)
    C = A @ A.T
    v1 = logdet(C, 'chol')
    v2 = np.log(np.linalg.det(C))
    assert np.allclose(v1, v2, atol=1e-8)

def test_negative_determinant_different():
    A = np.array([[-4,0],[0,-2]])
    v = logdet(A)
    expected = np.log(np.abs(np.linalg.det(A)))
    assert np.allclose(v, expected, atol=1e-10)

def test_complex_matrix_error_alt():
    A = np.array([[2+2j,1],[0,3]])
    with pytest.raises(ValueError, match="logdet:invalidarg"):
        logdet(A)