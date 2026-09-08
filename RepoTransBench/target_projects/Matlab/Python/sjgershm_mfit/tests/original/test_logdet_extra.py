import pytest
import numpy as np
from src.logdet import logdet

def test_large_random_positive_definite():
    np.random.seed(1)
    A = np.random.rand(5,5)
    C = A @ A.T
    v1 = logdet(C, 'chol')
    v2 = np.log(np.linalg.det(C))
    assert np.allclose(v1, v2, atol=1e-8)

def test_negative_determinant():
    A = np.array([[-2,0],[0,-3]])
    v = logdet(A)
    expected = np.log(np.abs(np.linalg.det(A)))
    assert np.allclose(v, expected, atol=1e-10)

def test_complex_matrix_error():
    A = np.array([[1+1j,2],[3,4]])
    with pytest.raises(ValueError, match="logdet:invalidarg"):
        logdet(A)