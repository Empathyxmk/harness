import pytest
from src.codeblocks.colors import colorToHex, NAME_TO_HEX

def test_colorToHex_6_digit_hex():
    assert colorToHex('#12abcd') == '#12abcd'

def test_colorToHex_3_digit_hex():
    assert colorToHex('#abc') == '#aabbcc'

def test_colorToHex_color_names():
    assert colorToHex('blue') == '#0000ff'

def test_colorToHex_unknown_colorname():
    assert colorToHex('unknowncolor') == 'unknowncolor'

def test_colorToHex_invalid_hex():
    assert colorToHex('#abcd') == '#abcd'

def test_colorToHex_non_string():
    assert colorToHex(123) == 123