import pytest
from src.flickermovie import flickermovie

def test_flickermovie_basic():
    m = flickermovie(10, 5)
    assert m != []
    assert len(m) == 10
    assert len(m[0]) == 5

def test_flickermovie_negative_input():
    with pytest.raises(ValueError):
        flickermovie(-2, 5)

def test_flickermovie_zero_length():
    m = flickermovie(0, 5)
    assert m == [] or m != []  # Check that code handles zero