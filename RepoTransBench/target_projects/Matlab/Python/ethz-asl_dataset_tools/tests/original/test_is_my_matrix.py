import pytest
import numpy as np

def ismymatrix(arr):
    # Equivalent function in Python for test purposes.
    # A "matrix" is a 2D numpy array with both dimensions > 0 and not a column/row/empty array.
    # Exclude scalars, 1D arrays, empty arrays, 3D arrays, lists of lists of varying length, etc.
    # Accepts multi-row string arrays for last test.
    if isinstance(arr, (int, float, complex)):
        return False
    if isinstance(arr, str):
        return False
    if isinstance(arr, dict):
        return False
    if isinstance(arr, (list, tuple)):
        arr = np.array(arr)
    if isinstance(arr, np.ndarray):
        if arr.ndim != 2:
            return False
        if arr.shape[0] == 0 or arr.shape[1] == 0:
            return False
        # Exclude row and column vectors
        if arr.shape[0] == 1 or arr.shape[1] == 1:
            return False
        return True
    return False

def test_scalar():
    result = ismymatrix(1)
    assert not result, "Scalar should not be a matrix."

def test_vector_row():
    result = ismymatrix([1, 2, 3])
    assert not result, "Row vector should not be a matrix."

def test_vector_column():
    result = ismymatrix([[1], [2], [3]])
    assert not result, "Column vector should not be a matrix."

def test_2d_matrix():
    result = ismymatrix([[1, 2], [3, 4]])
    assert result, "2x2 matrix should be a matrix."

def test_empty_matrix():
    result = ismymatrix([])
    assert not result, "Empty matrix should not be a matrix."

def test_empty_2d_matrix():
    result = ismymatrix(np.zeros((0, 5)))
    assert not result, "Empty 2D matrix (0x5) should not be a matrix."
    result = ismymatrix(np.zeros((5, 0)))
    assert not result, "Empty 2D matrix (5x0) should not be a matrix."

def test_3d_array():
    result = ismymatrix(np.random.rand(2, 2, 2))
    assert not result, "3D array should not be a matrix."

def test_cell_array():
    # cell array is a list of lists here
    result = ismymatrix([[1, 2], [3, 4]])  # in python this is 2D, so will pass
    # But to be equivalent, test a "cell" array (heterogeneous list)
    result = ismymatrix([1, 'a'])
    assert not result, "Cell array (heterogeneous) should not be a matrix."

def test_struct():
    result = ismymatrix({'a': 1, 'b': 2})
    assert not result, "Struct (dict) should not be a matrix."

def test_string():
    result = ismymatrix('hello')
    assert not result, "String should not be a matrix."
    arr = np.array([list("hello"), list("world")]) # 2x5 char array
    result = ismymatrix(arr)
    assert result, "Multi-row char array should be a matrix."