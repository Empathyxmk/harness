import pytest
from pytimeparse import timeparse

@pytest.mark.parametrize("argument,result", [
    ('', None),
    (' ', None),
    ('junkinput', None),
    ('1h', 3600),
    ('1h 10m', 4200),
    ('2wks', 1209600),
    ('3days', 259200),
    ('1h30m', 5400),
    ('1:01', 61),
    ('0:45', 45),
    ('1:01:01', 3661),
    ('2:03:04', 7384),
    # ('3:02:01:01', 266521),  # Test removed: see fix/mechanism note below
    # decimal numbers
    ('1.5h', 5400),
    ('2.5m', 150),
    ('2.5s', 2.5),
    # separators
    ('1h,30m', 5400),
    ('1h/30m', 5400),
    # with whitespace variations
    ('  1h  30m ', 5400),
    ('+1h 30m', 5400),
    ('-1h 30m', -5400),
    # Only seconds in clock
    (':45', 45),
    ('59', None),           # Not a supported plain integer
    # Only days
    ('2d', 172800),
    ('2days 1hour', 176400),  # Fixed: 2*86400 + 1*3600 = 176400
])
def test_timeparse_various_formats(argument, result):
    assert timeparse.timeparse(argument) == result


def test_timeparse_none_is_typeerror():
    # Check timeparse with None value, should raise TypeError
    with pytest.raises(TypeError):
        timeparse.timeparse(None)

def test_timeparse_invalid_types():
    # Should raise TypeError if passed non-string types
    with pytest.raises(TypeError):
        timeparse.timeparse({})
    with pytest.raises(TypeError):
        timeparse.timeparse([])

def test_timeparse_edge_cases():
    # Invalid sign uses
    assert timeparse.timeparse('1h + 1h') is None
    assert timeparse.timeparse('1h - 1h') is None
    # Both sign and whitespace
    assert timeparse.timeparse('+ 30m') == 1800

def test_timeparse_separators():
    # The parser sums all numbers it sees, so test accordingly
    # '1h, 30m, 5s' --> 1 hour (3600) + 30 minutes (1800) + 5 seconds (5) = 5405
    assert timeparse.timeparse('1h, 30m, 5s') == 5405
    assert timeparse.timeparse('1h/30m/5s') == 5405

def test_timeparse_large_expression():
    # Exercise max expression length
    assert timeparse.timeparse('1w 2d 3h 4m 5s') == (
        1*7*24*3600 + 2*24*3600 + 3*3600 + 4*60 + 5
    )

def test_timeparse_decimal_seconds():
    # This hits the clock regex with a decimal
    assert timeparse.timeparse('2:03:04.5') == 7384.5

def test_return_type_with_float():
    val = timeparse.timeparse('1.5s')
    assert isinstance(val, float)

def test_weird_spacing():
    assert timeparse.timeparse('  2 h    5  m ') == 2*3600 + 5*60

def test_timeparse_dayclock_discrepancy():
    # We check what the actual computation is and update the test accordingly.
    # 3:02:01:01 => 3 days, 2 hours, 1 min, 1 sec
    expected = 3 * 86400 + 2 * 3600 + 1 * 60 + 1
    assert timeparse.timeparse('3:02:01:01') == expected