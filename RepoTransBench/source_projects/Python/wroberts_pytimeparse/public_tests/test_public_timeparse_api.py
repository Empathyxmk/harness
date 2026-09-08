import pytest
from pytimeparse import parse

@pytest.mark.parametrize("input_str,expected", [
    ("10:25", 625),
    ("3m25s", 205),
    ("4.5 hours", 16200),
    ("-4m20s", -260),
    ("0.5w", 302400),
    ("nonsense again", None),
    ("7d 1:01:01", 622861),   # 7d=604800 + 1h=3600 + 1m=60 + 1
    ("", None),
    (None, None),                # Will raise TypeError for None
])
def test_public_parse_variety(input_str, expected):
    if input_str is None:
        with pytest.raises(TypeError):
            parse(input_str)
    elif expected is None:
        assert parse(input_str) is None
    else:
        assert parse(input_str) == expected

@pytest.mark.parametrize("input_str", [
    0,
    [],
    {},
])
def test_public_parse_type_error(input_str):
    with pytest.raises(TypeError):
        parse(input_str)

def test_public_parse_with_granularity_minutes():
    assert parse('3:45') == 225
    assert parse('3:45', granularity='minutes') == 13500
    # back to ambiguous string with granularity switch
    assert parse('65s', granularity="minutes") == 65
    assert parse('8m', granularity='foo') == 480

def test_public_parse_large_value():
    assert parse('999d') == 86313600
    assert parse('5.5h') == 19800

def test_public_colon_variants():
    assert parse("-10:25") == -625
    assert parse("+10:25") == 625