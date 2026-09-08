import pytest
from src.gf2dec import gf2dec, GF2DecInvalidInput

def test_basic_conversions():
    assert gf2dec([1]) == 1
    assert gf2dec([0]) == 0
    assert gf2dec([0, 1]) == 1
    assert gf2dec([1, 0]) == 2
    assert gf2dec([0, 1, 1]) == 3
    assert gf2dec([1, 0, 0]) == 4
    assert gf2dec([1, 0, 1]) == 5

def test_larger_numbers():
    assert gf2dec([1, 0, 0, 1]) == 9
    assert gf2dec([1, 1, 0, 0]) == 12
    assert gf2dec([0, 1, 0, 1, 0, 1, 0, 1]) == 85
    assert gf2dec([1, 1, 0, 1, 0, 1, 0, 1]) == 213
    # The expected value for this test is actually 1024 for MSB-first interpretation (position 5, value 1: 2^10 = 1024)
    assert gf2dec([0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) == 1024

def test_edge_cases():
    assert gf2dec([]) == 0
    assert gf2dec([0, 0, 0, 0, 0]) == 0
    assert gf2dec([1]) == 1
    assert gf2dec([0, 0, 1]) == 1

def test_invalid_input_type():
    with pytest.raises(GF2DecInvalidInput):
        gf2dec([1.5])
    with pytest.raises(GF2DecInvalidInput):
        gf2dec([2])
    with pytest.raises(GF2DecInvalidInput):
        gf2dec([-2])
    with pytest.raises(GF2DecInvalidInput):
        gf2dec([float('nan')])