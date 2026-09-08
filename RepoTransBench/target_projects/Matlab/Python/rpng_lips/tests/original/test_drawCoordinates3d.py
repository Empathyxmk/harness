import pytest
import numpy as np

from src.lips.drawCoordinates3d import drawCoordinates3d

def test_draw_at_origin():
    h = drawCoordinates3d(np.array([0, 0, 0]))
    assert hasattr(h, "figure") or hasattr(h, "axes")

def test_draw_at_point():
    h = drawCoordinates3d(np.array([1, 2, 3]))
    assert hasattr(h, "figure") or hasattr(h, "axes")

def test_draw_with_axes_length():
    h = drawCoordinates3d(np.array([1, 2, 3]), 2)
    assert hasattr(h, "figure") or hasattr(h, "axes")