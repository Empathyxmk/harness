import numpy as np
from src.pidmd import piDMD

def test_pidmd_public():
    # PUBLIC: piDMD functionality test with different random sizes
    np.random.seed(101)
    X1 = np.random.randn(4, 6)
    X2 = np.random.randn(4, 6)
    A = piDMD(X1, X2)
    X2_pred = A @ X1
    assert A.shape == (4, 4)
    assert X2_pred.shape == X2.shape