import re
from pytimeparse import timeparse

def test_weeks_regex():
    for val in ['2w', '2wk', '2wks', '2weeks']:
        match = re.match(timeparse.WEEKS, val)
        assert match is not None
        assert match.group('weeks') == '2'

def test_days_regex():
    for val in ['4d', '4dy', '4dys', '4days']:
        match = re.match(timeparse.DAYS, val)
        assert match is not None
        assert match.group('days') == '4'
    match = re.match(timeparse.DAYS, '1.5days')
    assert match.group('days') == '1.5'

def test_hours_regex():
    for val in ['7h', '7hr', '7hrs', '7hour', '7hours']:
        match = re.match(timeparse.HOURS, val)
        assert match is not None
        assert match.group('hours') == '7'
    # decimal hours
    match = re.match(timeparse.HOURS, '2.5hrs')
    assert match.group('hours') == '2.5'

def test_mins_regex():
    for val in ['9m', '9min', '9mins', '9minute', '9minutes']:
        match = re.match(timeparse.MINS, val)
        assert match is not None
        assert match.group('mins') == '9'
    # decimal minutes
    match = re.match(timeparse.MINS, '0.5min')
    assert match.group('mins') == '0.5'

def test_secs_regex():
    for val in ['15s', '15sec', '15secs', '15second', '15seconds']:
        match = re.match(timeparse.SECS, val)
        assert match is not None
        assert match.group('secs') == '15'
    # decimal seconds
    match = re.match(timeparse.SECS, '3.25s')
    assert match.group('secs') == '3.25'

def test_minclock_regex():
    m = re.match(timeparse.MINCLOCK, '3:09')
    assert m is not None
    assert m.group('mins') == '3'
    assert m.group('secs') == '09'
    # decimal seconds
    m = re.match(timeparse.MINCLOCK, '5:30.5')
    assert m is not None
    assert m.group('mins') == '5'
    assert m.group('secs') == '30.5'

def test_hourclock_regex():
    m = re.match(timeparse.HOURCLOCK, '10:23:59')
    assert m is not None
    assert m.group('hours') == '10'
    assert m.group('mins') == '23'
    assert m.group('secs') == '59'
    m = re.match(timeparse.HOURCLOCK, '1:01:01.1')
    assert m is not None
    assert m.group('hours') == '1'
    assert m.group('mins') == '01'
    assert m.group('secs') == '01.1'

def test_dayclock_regex():
    m = re.match(timeparse.DAYCLOCK, '2:10:23:12')
    assert m is not None
    assert m.group('days') == '2'
    assert m.group('hours') == '10'
    assert m.group('mins') == '23'
    assert m.group('secs') == '12'
    # with decimal seconds
    m = re.match(timeparse.DAYCLOCK, '2:10:23:12.249')
    assert m is not None
    assert m.group('secs') == '12.249'