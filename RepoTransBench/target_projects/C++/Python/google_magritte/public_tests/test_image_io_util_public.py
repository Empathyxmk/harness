import pytest

def test_alternate_image_size():
    # Instead of 2x2 or default, use 10x10
    width = 10
    height = 10
    pixels = width * height
    assert pixels == 100, "Public test image size not as expected"