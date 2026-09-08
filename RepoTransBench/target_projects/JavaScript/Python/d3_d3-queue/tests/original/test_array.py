import pytest
from src.d3_queue import array

def test_slice_regular_indices():
    arr = [1, 2, 3, 4]
    result = array.slice(arr, 1, 3)
    assert result == [2, 3]

def test_slice_clone():
    arr = [9, 10]
    result = array.slice(arr)
    assert result == [9, 10]