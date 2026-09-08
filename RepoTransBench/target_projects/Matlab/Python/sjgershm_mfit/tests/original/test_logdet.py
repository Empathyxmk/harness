import pytest
import numpy as np
from src.logdet import logdet

def test_square_matrix_lu():
    A = np.array([[2,1],[1,4]])
    v1 = logdet(A)
    v2 = np.log(np.linalg.det(A))
    assert np.allclose(v1, v2, atol=1e-10)

def test_square_matrix_chol():
    A = np.array([[4,2],[2,5]])
    v1 = logdet(A, 'chol')
    v2 = np.log(np.linalg.det(A))
    assert np.allclose(v1, v2, atol=1e-10)

def test_singular_matrix():
    A = np.array([[1,2],[2,4]])
    v = logdet(A)
    assert np.isinf(v) and v < 0

def test_non_square_matrix_error():
    A = np.array([[1,2,3],[4,5,6]])
    with pytest.raises(ValueError, match="logdet:invalidarg"):
        logdet(A)

def test_wrong_op_arg_error():
    A = np.eye(2)
    with pytest.raises(ValueError, match="logdet:invalidarg"):
        logdet(A, "not_chol")