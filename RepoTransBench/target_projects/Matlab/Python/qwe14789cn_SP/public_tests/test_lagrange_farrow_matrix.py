import pytest
from src.sp import lagrange_farrow_matrix
import numpy as np

def test_order2():
    h = lagrange_farrow_matrix(2, 0.2)
    assert h.shape == (1,2)

def test_order3():
    h = lagrange_farrow_matrix(3, 0.7)
    assert h.shape == (1,3)

def test_order4():
    h = lagrange_farrow_matrix(4, 0.5)
    assert h.shape == (1,4)