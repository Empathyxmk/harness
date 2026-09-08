import numpy as np
from ukfmanifold.quaternions import isq

def test_row_vector():
    q = np.array([[1,2,3,4]])
    assert isq(q) == 2

def test_column_vector():
    q = np.array([[1],[2],[3],[4]])
    assert isq(q) == 1

def test_square_matrix_4x4():
    q = np.ones((4,4))
    assert isq(q) == 3

def test_not_quaternion_shape():
    q = np.ones((3,10))
    assert isq(q) == 0