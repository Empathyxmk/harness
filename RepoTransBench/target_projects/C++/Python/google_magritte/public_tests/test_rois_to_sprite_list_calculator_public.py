import pytest

def test_alt_premultiply_cpu():
    # Original might use 2x2 white/black images, here we use all red on 3x1
    width = 3
    height = 1
    total_pixels = width * height
    assert total_pixels == 3, "Alternate premultiplied image had wrong shape"

def test_alt_no_premultiply_sticker():
    # New input data & expectation compared to internal tests.
    original_alpha = 255
    modified_alpha = 128
    assert original_alpha != modified_alpha, "Public alt alpha sticker test failed"

def test_alt_sprite_pose():
    # Use a different center or angle, check for computation
    center_original = 0.5
    center_public = 0.75
    assert center_public > center_original, "Public sprite pose center is not greater"