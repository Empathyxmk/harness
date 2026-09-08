from honcho.colour import get_colour

def test_public_get_colour_values():
    # Use different names than original tests
    assert isinstance(get_colour("zebra"), int)
    assert isinstance(get_colour("lemon"), int)
    assert get_colour("zebra") == get_colour("zebra")
    assert get_colour("lemon") == get_colour("lemon")
    assert get_colour("zebra") != get_colour("lemon")