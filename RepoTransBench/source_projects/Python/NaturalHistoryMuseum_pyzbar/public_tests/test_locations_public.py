import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pyzbar.locations import polygon_from_bbox, Rect

def test_polygon_from_bbox_public():
    # Use a different bounding box
    bbox = (3, 4, 16, 22)
    polygon = polygon_from_bbox(bbox)
    # Polygon goes clockwise
    assert polygon == [Rect(3, 4), Rect(16, 4), Rect(16, 22), Rect(3, 22)]

def test_polygon_from_bbox_zero_width_height_public():
    bbox = (10, 10, 10, 25)
    polygon = polygon_from_bbox(bbox)
    assert polygon == [Rect(10, 10), Rect(10, 10), Rect(10, 25), Rect(10, 25)]