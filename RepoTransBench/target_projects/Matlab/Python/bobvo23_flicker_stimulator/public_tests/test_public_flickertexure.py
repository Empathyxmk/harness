import pytest
from src.flickermovie import flickermovie

def test_public_flickermovie_shape():
    tex = flickermovie(6, 4)
    assert tex != []

def test_public_flickermovie_double_zero():
    tex = flickermovie(0, 0)
    assert tex == []

def test_public_flickermovie_negative_dimension():
    with pytest.raises(ValueError):
        flickermovie(-1, 2)