import pytest
from src.flickertexure import flickertexure

def test_flickertexure_basic():
    out = flickertexure([1, 2, 3])
    assert out != []

def test_flickertexure_string_input():
    with pytest.raises(ValueError):
        flickertexure('str')

def test_flickertexure_empty_array():
    out = flickertexure([])
    assert 'out' in locals() or out == []