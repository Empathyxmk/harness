import pytest
from src.flickerTexture import flickerTexture

def test_public_flickerTexture_different_size():
    tex = flickerTexture(120, 120, 60)
    assert isinstance(tex, list) and len(tex) >= 1

def test_public_flickerTexture_negative_size():
    with pytest.raises(ValueError):
        flickerTexture(-10, 120, 60)

def test_public_flickerTexture_minimal():
    tex = flickerTexture(10, 10, 1)
    assert isinstance(tex, list)