import pytest
import pytz
from datetime import datetime, timedelta
from delorean.interface import Delorean
from delorean.exceptions import DeloreanInvalidTimezone

def test_delorean_constructor_naive():
    dt = datetime(2022, 1, 2, 12, 0, 0)
    d = Delorean(dt, timezone='UTC')
    assert d.datetime == pytz.UTC.localize(dt)
    assert d.tz.zone == 'UTC'

def test_delorean_constructor_timezone_str_and_obj():
    dt = datetime(2022, 1, 2, 13, 0, 0)
    d1 = Delorean(dt, timezone='US/Pacific')
    assert d1.tz.zone == 'US/Pacific'
    d2 = Delorean(dt, timezone=pytz.timezone('US/Eastern'))
    assert d2.tz.zone == 'US/Eastern'

def test_delorean_constructor_invalid_timezone():
    dt = datetime(2022, 1, 2, 13, 0, 0)
    with pytest.raises(DeloreanInvalidTimezone):
        Delorean(dt, timezone='Invalid/Zone')

def test_delorean_shift_minutes_and_seconds():
    d = Delorean(datetime(2017, 5, 6, 12, 30, 0), timezone='UTC')
    d2 = d.shift(minutes=2, seconds=5)
    assert d2.datetime.minute == 32
    assert d2.datetime.second == 5

def test_delorean_next_last_methods():
    d = Delorean(datetime(2021, 12, 31, 23, 0, 0), timezone='UTC')
    next_day = d.next_day()
    assert next_day.datetime.day == 1 or next_day.datetime.month == 1

    last_week = d.last_week()
    assert (0 <= (d.datetime - last_week.datetime).days <= 7)

def test_delorean_truncate_to_day():
    d = Delorean(datetime(2022, 3, 4, 15, 34, 56), timezone='UTC')
    truncated = d.truncate('day')
    assert truncated.datetime.hour == 0
    assert truncated.datetime.minute == 0

def test_delorean_eq_and_repr():
    d1 = Delorean(datetime(2022, 3, 4, 0, 0, 0), timezone='UTC')
    d2 = Delorean(datetime(2022, 3, 4, 0, 0, 0), timezone='UTC')
    assert d1 == d2
    assert 'Delorean' in repr(d1)

def test_delorean_rollforward_rollbackup():
    d = Delorean(datetime(2022, 3, 6, 0, 0, 0), timezone='UTC')
    rf = d.rollforward('Monday')
    rb = d.rollback('Monday')
    assert hasattr(rf, 'datetime')
    assert hasattr(rb, 'datetime')
    assert rf != d or rb != d  # could land on the same if already Monday

def test_delorean_timezone_and_convert():
    d = Delorean(datetime(2021, 3, 1, 10, 0, 0), timezone='UTC')
    local = d.localize('US/Pacific')
    assert local.tz.zone == 'US/Pacific'
    norm = d.normalize('US/Pacific')
    assert norm.tz.zone == 'US/Pacific'
    # to_unix, to_pytz, to_datetime
    assert isinstance(d.to_unix(), float)
    assert d.to_pytz().tzinfo is not None
    assert d.to_datetime().tzinfo is not None

def test_delorean_convert_unsupported():
    d = Delorean(datetime(2022, 1, 1, 0, 0, 0), timezone='UTC')
    with pytest.raises(ValueError):
        d.truncate('unknown')

def test_delorean_factory_methods():
    # utcnow, now, parse, epoch
    d1 = Delorean.utcnow()
    d2 = Delorean.now('UTC')
    d3 = Delorean.parse('2021-01-01T10:00:00Z')
    d4 = Delorean.epoch(0, timezone='UTC')
    assert isinstance(d1, Delorean)
    assert isinstance(d2, Delorean)
    assert isinstance(d3, Delorean)
    assert isinstance(d4, Delorean)
    assert d4.datetime.year == 1970