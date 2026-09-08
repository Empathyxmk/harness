import pytest
import numpy as np

from src.cursorloc.cursorLocation import cursorLocation

def test_basic_valid():
    img = np.zeros((100, 100))
    x, y = cursorLocation(img, (50, 50))
    assert (x, y) == (50, 50)

def test_non_central():
    img = np.zeros((10, 10))
    x, y = cursorLocation(img, (2, 8))
    assert (x, y) == (2, 8)

def test_edge_values():
    img = np.ones((3, 3))
    x, y = cursorLocation(img, (1, 3))
    assert x == 1
    assert y == 3

def test_throws_error_on_size():
    img = np.zeros((5, 5))
    with pytest.raises(Exception):
        cursorLocation(img, (1, 2, 3))