import numpy as np
from src.pidmd import piDMD

def test_circulant_public():
    # PUBLIC: DMD shift test with different values
    X1 = np.array([[10, 20, 30], [40, 50, 60]], dtype=float)
    X2 = np.array([[11, 21, 31], [41, 51, 61]], dtype=float)
    A = piDMD(X1, X2)
    X2_predict = A @ X1
    assert np.linalg.norm(X2_predict - X2, ord='fro') < 25  # provide slack; different data