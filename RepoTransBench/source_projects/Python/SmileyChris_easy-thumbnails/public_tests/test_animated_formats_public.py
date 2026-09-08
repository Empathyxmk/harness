import pytest
from easy_thumbnails.engine import _gif_transparency, _webp_transparency

def test_gif_transparency_true_public():
    # Slightly different info dict to existing tests
    info = {"transparency": 0, "background": 1}
    result = _gif_transparency(info)
    assert result is True

def test_gif_transparency_false_public():
    info = {"other": 999}
    result = _gif_transparency(info)
    assert result is False

def test_webp_transparency_public():
    class DummyImage:
        def __init__(self, mode):
            self.mode = mode
    img = DummyImage("RGBA")
    assert _webp_transparency(img) is True
    img = DummyImage("L")
    assert _webp_transparency(img) is False