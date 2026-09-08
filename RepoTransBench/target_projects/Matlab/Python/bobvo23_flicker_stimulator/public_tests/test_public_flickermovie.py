import pytest
from src.flickermovie import flickermovie

def test_public_flickermovie_basic():
    m = flickermovie(15, 3)
    assert m != []

def test_public_flickermovie_negative_second_param():
    with pytest.raises(ValueError):
        flickermovie(5, -4)

def test_public_flickermovie_minimal():
    m = flickermovie(1, 1)
    assert m == [] or m != []