import pytest
import numpy as np
from src.sp import capon_doa_est

def test_small_input():
    y = np.array([1+1j, 2+2j, 3+3j])
    doa = capon_doa_est(y, 3, 1)
    assert len(doa) == 1

def test_matrix_input():
    y = np.tile(np.array([[1],[2],[3],[4]]), (1,2))
    doa = capon_doa_est(y, 4, 2)
    assert len(doa) == 2