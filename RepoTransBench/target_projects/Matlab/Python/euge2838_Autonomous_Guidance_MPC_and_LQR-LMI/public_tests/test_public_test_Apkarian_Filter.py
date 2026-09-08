import pytest
import numpy as np

def Apkarian_Filter(A, B, C, D, order):
    N = np.array(A)
    M = np.array(B).reshape(N.shape[0], -1)
    return N, M

def test_public_test_Apkarian_Filter():
    A = np.array([[2, 0], [1, 5]])
    B = np.array([[3], [4]])
    C = np.array([1, 6])
    D = 2
    order = 3

    N, M = Apkarian_Filter(A, B, C, D, order)
    assert N.shape == (2, 2)
    assert M.shape == (2, 1)