import pytest
from src.gf2dec import gf2dec, GF2DecInvalidInput

def test_basic_conversions():
    # Test basic binary (MSB first) to decimal
    assert gf2dec([0]) == 0
    assert gf2dec([1]) == 1
    assert gf2dec([1, 0]) == 2
    assert gf2dec([0, 1]) == 1
    assert gf2dec([1, 1]) == 3
    assert gf2dec([1, 0, 1]) == 5
    assert gf2dec([0, 0, 0, 1]) == 1

def test_larger_numbers():
    assert gf2dec([1, 1, 1, 1]) == 15
    assert gf2dec([1, 0, 0, 0, 0, 0, 0, 0]) == 128
    assert gf2dec([1, 0, 1, 0, 1, 0, 1, 0]) == 170
    # Test padding with leading zeros (should be 128)
    assert gf2dec([0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]) == 128

def test_edge_cases():
    assert gf2dec([]) == 0
    assert gf2dec([0, 0, 0, 0]) == 0
    assert gf2dec([0]) == 0
    assert gf2dec([1]) == 1

def test_invalid_input_type():
    with pytest.raises(GF2DecInvalidInput):
        gf2dec([0.5])
    with pytest.raises(GF2DecInvalidInput):
        gf2dec([2])
    with pytest.raises(GF2DecInvalidInput):
        gf2dec([3])
    with pytest.raises(GF2DecInvalidInput):
        gf2dec([-1])
    with pytest.raises(GF2DecInvalidInput):
        gf2dec(['a'])