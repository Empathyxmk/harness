import pytest
import numpy as np
from src.channel_estimation.coeffes2_MlN import coeffes2_MlN

def test_MlN_Basic():
    H1_mtx_es = np.eye(2)
    K = 3
    coeff = np.array([[2, 3, 4], [1, 2, 1]])
    H1_mtx = np.eye(2)
    H_drl_es = np.ones((2, 3))
    H_drl = np.zeros((2, 3))
    result = coeffes2_MlN(H1_mtx_es, K, coeff, H1_mtx, H_drl_es, H_drl)
    expected = np.array([
        [0, 1, 2],
        [0, 1, 0]
    ])
    np.testing.assert_array_equal(result, expected)

def test_MlN_DifferentShapes():
    H1_mtx_es = np.eye(1)
    K = 2
    coeff = np.array([[5, 7], [1, 3]])
    H1_mtx = np.eye(2)
    H_drl_es = np.ones((2, 2))
    H_drl = np.zeros((2, 2))
    with pytest.raises(ValueError):
        coeffes2_MlN(H1_mtx_es, K, coeff, H1_mtx, H_drl_es, H_drl)