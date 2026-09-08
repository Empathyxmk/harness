import pytest
from src.sp import lagrange_farrow_matrix
import numpy as np

def test_odd_length():
    h = lagrange_farrow_matrix(3)
    assert h.shape == (3, 3)
    assert isinstance(h, np.ndarray) and h.dtype == float

def test_even_length():
    h = lagrange_farrow_matrix(4)
    assert h.shape == (4, 4)

def test_matrix_sum():
    h = lagrange_farrow_matrix(3)
    s = np.sum(h)
    assert abs(s) < 1

def test_larger_l():
    h = lagrange_farrow_matrix(7)
    assert h.shape == (7, 7)