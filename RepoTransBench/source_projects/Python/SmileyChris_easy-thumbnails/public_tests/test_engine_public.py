import pytest
from easy_thumbnails import engine

def test_get_engine_by_name_public():
    assert engine.get_engine('PIL') == engine.pil_engine
    assert engine.get_engine('vil') == engine.vil_engine

def test_pil_engine_resize_public():
    img = engine.pil_engine.create_image((50, 40), 'RGB')
    resized = engine.pil_engine.scale_and_crop(img, (15, 8))
    assert resized.size == (15, 8)

def test_vil_engine_resize_public():
    img = engine.vil_engine.create_image((20, 20), 'RGB')
    cropped = engine.vil_engine.scale_and_crop(img, (10, 5), crop=True)
    assert cropped.size == (10, 5)