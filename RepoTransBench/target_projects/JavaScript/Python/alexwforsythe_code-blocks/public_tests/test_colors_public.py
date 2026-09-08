from src.codeblocks.colors import colorToHex, NAME_TO_HEX

def test_colorToHex_6_digit_hex_public():
    assert colorToHex('#abcdef') == '#abcdef'

def test_colorToHex_3_digit_hex_public():
    assert colorToHex('#123') == '#112233'

def test_colorToHex_color_names_public():
    assert colorToHex('red') == '#ff0000'

def test_colorToHex_unknown_colorname_public():
    assert colorToHex('notacolor') == 'notacolor'

def test_colorToHex_invalid_hex_public():
    assert colorToHex('#12ab') == '#12ab'

def test_colorToHex_non_string_public():
    assert colorToHex(False) is False