import pytest
from datetime import datetime, timedelta

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import delorean
from delorean import Delorean
from delorean.interface import parse, epoch, utcnow
from delorean.exceptions import DeloreanInvalidTimezone, DeloreanInvalidTime

def test_delorean_constructor_naive_public():
    dt = datetime(2022, 7, 14, 19, 15, 11)
    d = Delorean(dt, timezone="Asia/Singapore")
    assert d.datetime.year == 2022
    assert d.datetime.month == 7
    assert d.datetime.day == 14
    assert hasattr(d.tzinfo, "zone")
    assert d.tzinfo.zone.lower() in ["asia/singapore", "singapore"]

def test_delorean_constructor_aware_public():
    import pytz
    tz = pytz.timezone("Australia/Sydney")
    dt = tz.localize(datetime(2023, 1, 25, 23, 30, 3))
    d = Delorean(dt)
    assert d.datetime.year == 2023
    assert d.datetime.month == 1
    assert d.datetime.day == 25
    # zone might be 'Australia/Sydney' or an alias, allow for substring match
    assert any(zone in d.tzinfo.zone for zone in ["Sydney", "Australia"])

def test_delorean_str_public():
    d = Delorean(datetime(2021, 5, 8, 20, 48), timezone="America/Mexico_City")
    s = str(d)
    assert "delorean" in s.lower()
    assert "Mexico_City" in s or "Mexico" in s

def test_parse_string_public():
    d = parse("2024-01-12T13:22:05-04:00")
    assert d.datetime.year == 2024
    assert d.datetime.month == 1
    assert d.datetime.day == 12
    assert d.datetime.hour == 13
    assert d.tzinfo is not None

def test_parse_unix_epoch_public():
    ts = 1640995200  # 2022-01-01 00:00:00 UTC
    d = epoch(ts)
    assert d.datetime.year == 2022
    assert d.datetime.month == 1
    assert d.datetime.day == 1
    assert str(d.tzinfo).lower() in ("utc",)

def test_utcnow_public():
    d = utcnow()
    now = datetime.utcnow()
    diff = abs((d.datetime - now).total_seconds())
    assert diff < 5
    assert str(d.tzinfo).lower() in ("utc",)

def test_shift_public():
    d = Delorean(datetime(2031, 2, 14, 21, 32), timezone="Asia/Dubai")
    d2 = d.shift("Europe/London")
    assert hasattr(d2.tzinfo, "zone")
    assert "london" in d2.tzinfo.zone.lower()
    assert d2.datetime.year == 2031
    assert d2.datetime.month == 2

def test_truncate_public():
    d = Delorean(datetime(2019, 4, 15, 16, 14, 59), timezone="US/Pacific")
    d2 = d.truncate("month")
    assert d2.datetime.year == 2019
    assert d2.datetime.month == 4
    assert d2.datetime.day == 1

def test_next_previous_public():
    d = Delorean(datetime(2017, 6, 12, 21, 30), timezone="Europe/Bucharest")
    nex = d.next("month")
    prev = d.last("month")
    assert nex.datetime.month == 7
    assert prev.datetime.month == 5

def test_invalid_timezone_public():
    with pytest.raises(DeloreanInvalidTimezone):
        Delorean(datetime(2021, 8, 31), timezone="Never/Neverland")

def test_invalid_time_public():
    with pytest.raises(DeloreanInvalidTime):
        parse("not-a-time-string-xyz")

def test_comparisons_public():
    d1 = Delorean(datetime(2011, 11, 11), timezone="UTC")
    d2 = Delorean(datetime(2012, 12, 10), timezone="UTC")
    assert d1 < d2
    assert d2 > d1
    assert d1 != d2

def test_equality_timezone_public():
    d1 = Delorean(datetime(2008, 8, 8), timezone="Asia/Shanghai")
    d2 = Delorean(datetime(2008, 8, 8), timezone="Asia/Shanghai")
    assert d1 == d2

def test_add_subtract_timedelta_public():
    d = Delorean(datetime(2010, 12, 1, 10, 11), timezone="Europe/Istanbul")
    d2 = d + timedelta(days=3)
    d3 = d2 - timedelta(hours=12)
    assert d2.datetime.day == 4
    assert d3.datetime.day == 3
    assert d3.datetime.hour == 22

def test_min_max_public():
    d1 = Delorean(datetime(2017, 6, 1, 8, 0), timezone="Europe/Helsinki")
    d2 = Delorean(datetime(2017, 6, 2, 8, 0), timezone="Europe/Helsinki")
    assert max([d1, d2]) == d2
    assert min([d1, d2]) == d1