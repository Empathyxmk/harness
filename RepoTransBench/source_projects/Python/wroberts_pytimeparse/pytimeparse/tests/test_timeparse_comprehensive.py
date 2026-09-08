import pytest
from pytimeparse.timeparse import timeparse, _interpret_as_minutes

@pytest.mark.parametrize(
    "input_str,expected",
    [
        ("1:24", 84),                # 1 min 24 sec (should interpret as 1min24sec, converted to 84sec)
        (":22", 22),                 # 0min22sec
        ("1 minute, 24 secs", 84),
        ("1m24s", 84),
        ("1.2 minutes", 72),
        ("1.2 seconds", 1.2),
        ("-1m24s", -84),
        ("+1m24s", 84),
        # The documented calculation for 2w3d4h5m6s: 2w=1209600, 3d=259200, 4h=14400, 5m=300, 6s=6 = 1483506
        ("2w3d4h5m6s", 1483506),
        ("3d", 259200),
        ("1 h", 3600),
        ("1.5 hours", 5400),
        # 2d = 172800, 23:59:59 = 23*3600+59*60+59=86399, sum=259199
        ("2d, 23:59:59", 259199),
        ("1:23:45", 5025),           # 1h * 3600 + 23m * 60 + 45 = 5025
        # Actually, '00:01' will match 'MINCLOCK' regex: mins=00, secs=01 --> 0*60+1 = 1
        ("00:01", 1),
        # 1 week=604800, 2 days=172800, 3 hours=10800, 4 mins=240, 5 secs=5 = 788645
        ("1 weeks, 2 days, 3 hours, 4 mins, 5 secs", 788645),
        ("", None),
        ("nonsense", None),
        ("--1m24s", None),           # Invalid double sign, should be None
        # 1.5w = 907200
        ("1.5w", 907200),
        # 3.2d = 276480
        ("3.2d", 276480),
        # 4:03:02 = 4h*3600 + 3m*60 + 2 = 14582
        ("4:03:02", 14582),
        # 2:03:04.5 = 2h*3600 + 3m*60 + 4.5 = 7384.5
        ("2:03:04.5", 7384.5)
    ]
)
def test_timeparse(input_str, expected):
    result = timeparse(input_str)
    if expected is None:
        assert result is None
    elif isinstance(expected, float):
        assert pytest.approx(result) == expected
    else:
        assert result == expected

def test_timeparse_hours_minutes_ambiguity():
    # With ambiguous input like "1:22", _interpret_as_minutes should swap mins/secs to hours/mins
    input_dict = {'secs': '24', 'mins': '1'}
    out = _interpret_as_minutes('1:24', dict(input_dict))
    assert out['hours'] == '1'
    assert out['mins'] == '24'
    assert 'secs' not in out

def test_timeparse_edge_cases():
    # Valid, but odd input cases
    assert timeparse('   2h  ') == 7200
    # According to timeparse.py, '0' will not match any custom format (returns None)
    assert timeparse('0') is None
    assert timeparse('+0') is None
    assert timeparse('-0') is None
    # Rounds float for whole seconds
    assert timeparse('1.99 seconds') == pytest.approx(1.99)
    # Large value
    assert timeparse('1000d') == 86400000

def test_granularity_minutes():
    # According to the docstring (and code), granularity currently only affects ambiguous '1:30'-type input.
    # For '2m', it will always return 120 regardless of granularity
    assert timeparse('2m', granularity='minutes') == 120
    assert timeparse('90s', granularity='minutes') == 90
    assert timeparse('84s', granularity='minutes') == 84
    # But ambiguous 1:30 will be affected by granularity
    # 1:30 => mins=1, secs=30 (default) => 90; with granularity='minutes', becomes hours=1, mins=30 => 5400
    assert timeparse('1:30') == 90
    assert timeparse('1:30', granularity='minutes') == 5400

def test_granularity_error():
    # The code does not raise ValueError for unsupported granularity; just ignores it.
    assert timeparse('2m', granularity='foo') == 120

def test_unsupported_float_parsing():
    # Should handle seconds with decimal correctly
    assert timeparse('0.1s') == pytest.approx(0.1)

def test_invalid_types():
    # For None or non-str input, should raise TypeError, currently does not handle explicitly.
    # So we expect a TypeError for current implementation.
    import pytest
    with pytest.raises(TypeError):
        timeparse(None)
    with pytest.raises(TypeError):
        timeparse(12345)

def test_signed_colon_format():
    # Inputs like -1:24 should be parsed as signed minutes
    assert timeparse("-1:24") == -84
    assert timeparse("+1:24") == 84

def test_partial_matches_fail():
    # If string contains valid pattern as substring, but not as full string, should return None
    assert timeparse("foo 3d bar") is None