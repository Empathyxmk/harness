import pytest
from src.findindex import findindex

def test_public_find_index():
    A = [10, 21, 33, 40, 55]
    val = 33
    idx = findindex(val, A)
    assert idx == 3

    A = [7, 8, 9, 10]
    val = 8
    idx = findindex(val, A)
    assert idx == 2