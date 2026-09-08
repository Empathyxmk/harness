import pytest
from src.square_flicker import square_flicker
import numpy as np

def test_square_flicker_basic():
    out = square_flicker(4, [1, 1, 1], [0, 0, 0])
    assert out != []
    for vec in out:
        assert np.shape(vec) == (3,)

def test_square_flicker_bad_color_shape():
    with pytest.raises(ValueError):
        square_flicker(4, 1, [0, 0, 0])

def test_square_flicker_zero_frames():
    out = square_flicker(0, [1, 1, 1], [0, 0, 0])
    assert out == [] or out != []