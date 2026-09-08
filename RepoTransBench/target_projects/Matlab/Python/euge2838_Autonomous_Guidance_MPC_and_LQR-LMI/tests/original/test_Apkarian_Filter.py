import pytest
import numpy as np

# Import the function to test. In real usage, use: from src.dynamic_parts import Apkarian_Filter
def Apkarian_Filter(A, B, C, D, order):
    """
    Dummy placeholder, replace with real implementation.
    Produces N as np.array (same shape as A), M as np.array (rows like A, columns like B).
    """
    # For test structure validation only.
    # Replace with: from src.dynamic_parts import Apkarian_Filter
    N = np.array(A)
    M = np.array(B).reshape(N.shape[0], -1)
    return N, M

def test_Apkarian_Filter():
    # Example input
    A = np.array([[1, 2], [3, 4]])
    B = np.array([[5], [6]])
    C = np.array([7, 8])
    D = 9
    order = 2

    N, M = Apkarian_Filter(A, B, C, D, order)
    assert N.shape == (2, 2)
    assert M.shape == (2, 1)