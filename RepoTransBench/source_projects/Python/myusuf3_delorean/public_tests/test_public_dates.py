import pytest
import pytz
from datetime import datetime, timedelta
from delorean import dates

def test_get_total_second_basic_public():
    td = timedelta(hours=3, minutes=4, seconds=5, microseconds=8)
    expected = 3*3600 + 4*60 + 5 + 8e-6
    assert abs(dates.get_total_second(td) - expected) < 1e-6

def test_is_datetime_naive_public():
    dt = datetime(2005, 10, 11)
    assert dates.is_datetime_naive(dt)
    dt_aware = pytz.UTC.localize(dt)
    assert not dates.is_datetime_naive(dt_aware)

def test_is_datetime_instance_none_public():
    assert dates.is_datetime_instance(None) is None

def test_is_datetime_instance_wrong_type_public():
    with pytest.raises(ValueError):
        dates.is_datetime_instance("not-a-datetime")

def test_move_datetime_day_public():
    dt = datetime(2022, 6, 15)
    result = dates.move_datetime_day(dt, "next", 10)
    assert result.day == 25
    result2 = dates.move_datetime_day(dt, "last", 3)
    assert result2.day == 12

def test_move_datetime_hour_public():
    dt = datetime(2023, 2, 15, 13)
    result = dates.move_datetime_hour(dt, "next", 8)
    assert result.hour == 21
    result2 = dates.move_datetime_hour(dt, "last", 5)
    assert result2.hour == 8

def test_move_datetime_minute_public():
    dt = datetime(2022, 7, 4, 9, 10)
    result = dates.move_datetime_minute(dt, "next", 35)
    assert result.minute == 45

def test_move_datetime_second_public():
    dt = datetime(2021, 9, 20, 1, 5, 15)
    result = dates.move_datetime_second(dt, "next", 40)
    assert result.second == 55

def test_move_datetime_month_public():
    dt = datetime(2017, 11, 18)
    result = dates.move_datetime_month(dt, "next", 5)
    assert result.month == 4 and result.year == 2018
    result2 = dates.move_datetime_month(dt, "last", 1)
    assert (result2.month == 10 and result2.year == 2017)

def test_move_datetime_week_public():
    dt = datetime(2021, 3, 10)
    result = dates.move_datetime_week(dt, "next", 3)
    assert result.day in (17, 24, 31)  # 3 weeks later

def test_move_datetime_year_public():
    dt = datetime(2018, 12, 31)
    result = dates.move_datetime_year(dt, "next", 4)
    assert result.year == 2022
    result2 = dates.move_datetime_year(dt, "last", 2)
    assert result2.year == 2016

@pytest.mark.parametrize("current, target, direction, expected_days", [
    # dt = 2022-01-10 (Monday): next Thursday = 2022-01-13
    ("Monday", "Thursday", "next", 3),
    # dt = 2022-01-12 (Wednesday): last Monday = 2022-01-10
    ("Wednesday", "Monday", "last", -2),
    # dt = 2022-01-15 (Saturday): next Saturday = 2022-01-22
    ("Saturday", "Saturday", "next", 7),
    # dt = 2022-01-16 (Sunday): last Friday = 2022-01-14
    ("Sunday", "Friday", "last", -2),
])
def test_move_datetime_namedday_public(current, target, direction, expected_days):
    days = {
        'Monday': 10, 'Tuesday': 11, 'Wednesday': 12, 'Thursday': 13, 'Friday': 14, 'Saturday': 15, 'Sunday': 16
    }
    dt = datetime(2022, 1, days[current], 0, 0, 0)
    moved = dates.move_datetime_namedday(dt, direction, target)
    assert (moved - dt).days == expected_days

def test_datetime_timezone_and_localize_normalize_public():
    result = dates.datetime_timezone('Europe/Berlin')
    assert hasattr(result, 'tzinfo')
    assert result.tzinfo is not None

    naive_dt = datetime(2015, 12, 3)
    aware = dates.localize(naive_dt, 'US/Eastern')
    assert hasattr(aware, 'utcoffset')
    aware2 = dates.localize(naive_dt, pytz.timezone('US/Eastern'))
    assert hasattr(aware2, 'utcoffset')

def test_normalize_valid_public():
    d1 = pytz.timezone('Europe/London').localize(datetime(2018, 5, 5))
    normalized = dates.normalize(d1, 'US/Eastern')
    assert "Eastern" in str(normalized.tzinfo)

def test_normalize_invalid_timezone_public():
    d1 = pytz.timezone('UTC').localize(datetime(2020, 3, 17))
    with pytest.raises(Exception):
        dates.normalize(d1, 'No/ExistZone')