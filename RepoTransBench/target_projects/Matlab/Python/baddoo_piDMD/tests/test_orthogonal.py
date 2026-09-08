import numpy as np

def test_orthogonal():
    # Test orthogonality preservation in manually crafted transformation
    np.random.seed(123)
    X1 = np.linalg.qr(np.random.randn(6, 3))[0]
    Q = np.linalg.qr(np.random.randn(6, 3))[0]
    # Apply orthogonal transformation
    X2 = Q.T @ X1  # Corrected: (3,6) x (6,3) = (3,3)
    # Check that result is still orthogonal
    result = X2.T @ X2
    identity = np.eye(3)
    assert np.allclose(result, identity, atol=1e-12)