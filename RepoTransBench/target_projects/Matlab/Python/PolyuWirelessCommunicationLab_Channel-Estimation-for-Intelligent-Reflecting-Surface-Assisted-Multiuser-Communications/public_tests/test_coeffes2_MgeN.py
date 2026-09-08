import pytest
import numpy as np
from src.channel_estimation.coeffes2_MgeN import coeffes2_MgeN

def test_DiffSimple():
    H1_mtx_es = 2 * np.eye(2)
    K = 3
    coeff = np.array([[2,3,4],[3,4,5]])
    H1_mtx = 2 * np.eye(2)
    H_drl_es = np.ones((2,3))
    H_drl = np.zeros((2,3))
    result = coeffes2_MgeN(H1_mtx_es, K, coeff, H1_mtx, H_drl_es, H_drl)
    expected = np.zeros((2,3))
    expected[:, 0] = [2, 3]
    expected[:, 1] = [2.5, 3.5]
    expected[:, 2] = [3.5, 4.5]
    np.testing.assert_array_almost_equal(result, expected)

def test_DifferentSize():
    H1_mtx_es = np.array([[2,1]])
    K = 2
    coeff = np.array([[2,4],[3,7]])
    H1_mtx = np.array([[2,0],[0,1]])
    H_drl_es = np.ones((2,2))
    H_drl = 3 * np.ones((2,2))
    with pytest.raises(ValueError):
        coeffes2_MgeN(H1_mtx_es, K, coeff, H1_mtx, H_drl_es, H_drl)