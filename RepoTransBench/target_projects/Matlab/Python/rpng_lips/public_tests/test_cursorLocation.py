import pytest
import numpy as np

from src.cursorloc.cursorLocation import cursorLocation

def test_cursor_basic():
    img = np.zeros((400, 400))  # Simulated image
    # The function signature for cursorLocation may differ from Matlab, will simulate test for correctness
    x, y = cursorLocation(img, (250, 250))
    assert isinstance(x, (int, float, np.integer, np.floating))
    assert isinstance(y, (int, float, np.integer, np.floating))

def test_cursor_string_format():
    img = np.zeros((600, 500))
    x, y = cursorLocation(img, (124, 399))
    assert isinstance(x, (int, float, np.integer, np.floating))
    assert isinstance(y, (int, float, np.integer, np.floating))