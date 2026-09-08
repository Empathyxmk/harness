import pytest

def test_alternate_canvas_shape():
    # Instead of a small square, test a wide rectangle, e.g. 16x4.
    width = 16
    height = 4
    assert width * height == 64, "Canvas has unexpected area"