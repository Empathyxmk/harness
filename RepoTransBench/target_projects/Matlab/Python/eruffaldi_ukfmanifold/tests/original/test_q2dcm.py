import numpy as np
import pytest

from ukfmanifold.quaternions import q2dcm, qvxform, qnorm

def test_insufficient_arguments():
    with pytest.raises(TypeError):
        q2dcm()

def test_invalid_input_scalar():
    with pytest.raises(Exception):
        q2dcm(np.array([1.0]))

def test_ambiguous_input_4x4_non_normalized():
    arr = np.ones((4,4))
    # For now, just ensure function runs (warning not tested).
    q2dcm(arr)

def test_column_of_two_quaternions():
    Q = qnorm(2*np.random.rand(2,4)-1)
    v = np.array([1,2,3])
    A = q2dcm(Q)
    if A.shape == (3,3,2):
        result = np.vstack([A[:,:,0]@v, A[:,:,1]@v])
    else:
        result = np.vstack([A[0]@v, A[1]@v])
    truth = qvxform(Q, v)
    assert np.allclose(result, truth, atol=1e-12)

def test_row_of_two_quaternions():
    Q = qnorm(2*np.random.rand(4,2)-1)
    v = np.random.rand(3,2)
    A = q2dcm(Q)
    if A.shape == (3,3,2):
        result = np.column_stack([A[:,:,0]@v[:,0], A[:,:,1]@v[:,1]])
    else:
        result = np.column_stack([A[0]@v[:,0], A[1]@v[:,1]])
    truth = qvxform(Q, v)
    assert np.allclose(result, truth, atol=1e-12)