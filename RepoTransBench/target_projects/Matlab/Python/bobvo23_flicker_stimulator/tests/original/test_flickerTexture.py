import pytest
from src.flickerTexture import flickerTexture
import numpy as np

def test_flickerTexture_basic():
    ret = flickerTexture(10, [255, 255, 255], [0, 0, 0])
    assert ret != []

def test_flickerTexture_bad_input():
    with pytest.raises(TypeError):
        flickerTexture('bad', [1, 2, 3], [4, 5, 6])

def test_flickerTexture_size_variation():
    out = flickerTexture(5, [255, 255, 255], [0, 0, 0])
    assert out != []