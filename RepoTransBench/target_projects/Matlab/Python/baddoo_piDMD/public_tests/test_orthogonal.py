import numpy as np

def test_orthogonal_public():
    # PUBLIC: Test with different random orthogonal matrices
    np.random.seed(321)
    X1 = np.linalg.qr(np.random.randn(8, 4))[0]
    Q = np.linalg.qr(np.random.randn(8, 4))[0]
    X2 = Q.T @ X1  # Correct multiplication
    result = X2.T @ X2
    identity = np.eye(4)
    assert np.allclose(result, identity, atol=1e-12)