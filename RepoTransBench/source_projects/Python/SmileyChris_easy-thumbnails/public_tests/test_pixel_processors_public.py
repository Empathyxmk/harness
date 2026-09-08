import pytest
from easy_thumbnails.processors import scale_and_crop

def test_scale_and_crop_aspect_ratio_public():
    # Different size/aspect than original
    image_data = (70, 30)
    thumb_size = (20, 10)
    img = scale_and_crop.create_image(image_data, 'RGBA')
    thumb = scale_and_crop.scale_and_crop(img, thumb_size)
    assert thumb.size == thumb_size

def test_scale_and_crop_crop_option_public():
    img = scale_and_crop.create_image((60, 60), 'RGB')
    cropped = scale_and_crop.scale_and_crop(img, (20, 20), crop=True)
    assert cropped.size == (20, 20)