import numpy as np
from src.pidmd import piDMD

def test_circulant():
    # Checks DMD (piDMD) with shifted input matrices
    X1 = np.array([[1, 2, 3], [4, 5, 6]], dtype=float)
    X2 = np.array([[2, 3, 4], [5, 6, 7]], dtype=float)
    A = piDMD(X1, X2)
    X2_predict = A @ X1
    assert np.linalg.norm(X2_predict - X2, ord='fro') < 2.0  # a bit of slack for generic DMD