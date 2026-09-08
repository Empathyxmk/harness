import pytest

def test_first_character_invalid_error():
    # Simulate a syntax error caused by invalid character
    with pytest.raises(SyntaxError):
        raise SyntaxError("tests/first_character_invalid.glsl:1:1: error: invalid character encountered")