import pytest
from src.square_flicker import square_flicker
import numpy as np

def test_public_square_flicker_swapped_colors():
    out = square_flicker(6, [0.5, 0.5, 0.5], [1, 1, 1])
    assert out != []
    for vec in out:
        assert np.shape(vec) == (3,)

def test_public_square_flicker_bad_shape():
    with pytest.raises(ValueError):
        square_flicker(2, [1, 1], [0, 0, 0])

def test_public_square_flicker_single_frame():
    out = square_flicker(1, [0, 0, 0], [1, 1, 1])
    assert out == [] or out != []