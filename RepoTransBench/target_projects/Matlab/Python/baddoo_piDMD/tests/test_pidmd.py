import numpy as np
from src.pidmd import piDMD

def test_pidmd():
    # Test piDMD functionality (no constraint) with random matrices
    np.random.seed(42)
    X1 = np.random.randn(3, 5)
    X2 = np.random.randn(3, 5)
    A = piDMD(X1, X2)
    X2_pred = A @ X1
    assert A.shape == (3, 3)
    assert X2_pred.shape == X2.shape