import pytest
from mammoth import images

def test_embedded_public_returns_bytesio():
    rel = type("rel", (), {})()
    rel.target_ref = "img001"
    img = images.Embedded("img_data", rel)
    assert img.open() == "img_data"
    assert img.content_type() is None
    assert img.alt_text() is None

def test_images_are_distinct_public():
    rel1 = type("rel", (), {})()
    rel2 = type("rel", (), {})()
    rel1.target_ref = "img_a"
    rel2.target_ref = "img_b"
    img1 = images.Embedded("A", rel1)
    img2 = images.Embedded("B", rel2)
    assert img1 != img2
    assert hash(img1) != hash(img2)

def test_no_images_public():
    none_image = images._NO_IMAGE
    assert none_image.open() is None
    assert none_image.content_type() is None
    assert none_image.alt_text() is None