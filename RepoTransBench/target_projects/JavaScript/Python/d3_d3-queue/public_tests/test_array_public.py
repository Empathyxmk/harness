import pytest
from src.d3_queue import array

def test_slice_public_different_indices():
    arr = [5,6,7,8,9]
    result = array.slice(arr, 2, 4)
    assert result == [7, 8]

def test_slice_public_clone_different_array():
    arr = [21, 42]
    result = array.slice(arr)
    assert result == [21, 42]