import numpy as np
from tests.original.munkres_helper import munkres

def test_munkres_diagonal():
    A = np.array([[1, 2], [3, 4]])
    ass, cost = munkres(A)
    assert np.array_equal(ass, np.array([1, 2]))
    assert cost == 1 + 4

def test_munkres_nonsquare():
    B = np.random.rand(3, 2)
    ass2, cost2 = munkres(B)
    assert all(ass2[0:2] == np.array([1, 2]))