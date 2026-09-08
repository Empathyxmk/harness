import sys
import os
import pytest

# Ensure import works regardless of test folder location
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pyzbar.locations import bounding_box, Rect

def test_bounding_box_rect_public():
    # Use different Rect coordinates than existing test, but same structure
    pts = [Rect(5, 7), Rect(25, 7), Rect(25, 32), Rect(5, 32)]
    box = bounding_box(pts)
    assert box == (5, 7, 25, 32)
    # Mix order for robustness
    pts_reorder = [Rect(25, 32), Rect(25, 7), Rect(5, 32), Rect(5, 7)]
    box2 = bounding_box(pts_reorder)
    assert box2 == (5, 7, 25, 32)

def test_bounding_box_negative_coords_public():
    pts = [Rect(-12, -8), Rect(0, -8), Rect(0, 2), Rect(-12, 2)]
    assert bounding_box(pts) == (-12, -8, 0, 2)