import pytest
from pytimeparse.timeparse import timeparse, _interpret_as_minutes

@pytest.mark.parametrize(
    "input_str,expected",
    [
        ("2:50", 170),                      # Different time: 2 min 50 sec = 170 sec
        (":45", 45),                        # 0 min 45 sec
        ("2 minutes, 30 secs", 150),
        ("2m30s", 150),
        ("3.3 minutes", 198),
        ("2.3 seconds", 2.3),
        ("-2m30s", -150),
        ("+2m30s", 150),
        # 1w2d3h4m5s: 1w=604800, 2d=172800, 3h=10800, 4m=240, 5s=5 = 798645
        ("1w2d3h4m5s", 798645),
        ("5d", 432000),
        ("2 h", 7200),
        ("2.5 hours", 9000),
        # 4d = 345600, 11:59:59 = 11*3600+59*60+59=43199, sum=388799
        ("4d, 11:59:59", 388799),
        ("2:33:21", 9201),                    # 2h*3600 + 33m*60 + 21 = 9201
        ("10:00", 600),                       # minutes: 10, seconds: 0
        # 2 weeks=1209600, 3 days=259200, 4 hours=14400, 5 mins=300, 6 secs=6 = 1483506 (shift to 1 week = 604800, 1d=86400 ...)
        ("2 weeks, 1 day, 1 hour, 1 min, 0 secs", 788460),
        ("badinput", None),
        ("", None),
        ("--2m30s", None),
        ("0.25w", 151200),
        ("2.8d", 241920),
        ("5:07:06", 18426),
        ("1:03:04.5", 3784.5)
    ]
)
def test_public_timeparse(input_str, expected):
    result = timeparse(input_str)
    if expected is None:
        assert result is None
    elif isinstance(expected, float):
        assert pytest.approx(result) == expected
    else:
        assert result == expected

def test_public_timeparse_hours_minutes_ambiguity():
    input_dict = {'secs': '50', 'mins': '2'}
    out = _interpret_as_minutes('2:50', dict(input_dict))
    assert out['hours'] == '2'
    assert out['mins'] == '50'
    assert 'secs' not in out

def test_public_timeparse_edge_cases():
    assert timeparse('   4h  ') == 14400
    assert timeparse('00') is None
    assert timeparse('+00') is None
    assert timeparse('-00') is None
    assert timeparse('2.01 seconds') == pytest.approx(2.01)
    assert timeparse('333d') == 28771200

def test_public_granularity_minutes():
    assert timeparse('4m', granularity='minutes') == 240
    assert timeparse('45s', granularity='minutes') == 45
    assert timeparse('69s', granularity='minutes') == 69
    assert timeparse('2:45') == 165
    assert timeparse('2:45', granularity='minutes') == 9900

def test_public_granularity_error():
    assert timeparse('1m', granularity='foobar') == 60

def test_public_unsupported_float_parsing():
    assert timeparse('0.11s') == pytest.approx(0.11)

def test_public_invalid_types():
    import pytest
    with pytest.raises(TypeError):
        timeparse([])
    with pytest.raises(TypeError):
        timeparse(0.33)

def test_public_signed_colon_format():
    assert timeparse("-2:50") == -170
    assert timeparse("+2:50") == 170

def test_public_partial_matches_fail():
    assert timeparse("hello 5d world") is None