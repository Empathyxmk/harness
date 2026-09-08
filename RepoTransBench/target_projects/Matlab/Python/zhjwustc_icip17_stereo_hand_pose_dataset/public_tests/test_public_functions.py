import numpy as np

from src.handpose.rodrigues import rodrigues, rodrigues_with_angle

def test_rodrigues_with_new_vector():
    newRotVec = np.array([0.3, -0.1, 0.2])
    R, theta = rodrigues_with_angle(newRotVec)
    assert R.shape == (3, 3)
    assert np.isscalar(theta)
    assert np.all(np.isfinite(R))
    assert np.isfinite(theta)

def test_rodrigues_zero_vector_different_shape():
    Rz = rodrigues(np.zeros(3))
    assert np.allclose(Rz, np.eye(3))

def test_rodrigues_negative_rotation():
    negRotVec = np.array([-0.2, 0.2, -0.2])
    Rn, thetan = rodrigues_with_angle(negRotVec)
    assert Rn.shape == (3, 3)
    assert np.isscalar(thetan)