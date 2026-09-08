import pytest
import numpy as np

from src.lips.drawCoordinates3d import drawCoordinates3d

def test_with_different_origin_and_angles():
    o = np.array([10, -2, 8])
    a = np.array([np.pi / 3, np.pi / 5, np.pi / 7])
    length = 5
    h = drawCoordinates3d(o, a, length)
    assert hasattr(h, 'figure') or hasattr(h, 'axes')

def test_zero_length():
    o = np.array([2, 3, 1])
    a = np.array([0.2, 0.1, 0.4])
    length = 0
    h = drawCoordinates3d(o, a, length)
    assert hasattr(h, 'figure') or hasattr(h, 'axes')