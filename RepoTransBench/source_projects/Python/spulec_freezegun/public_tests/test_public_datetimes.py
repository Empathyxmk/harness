import time
import datetime
import pytest
from freezegun import freeze_time


def test_public_different_simple_api() -> None:
    freezer = freeze_time("2020-02-20")
    local_time = datetime.datetime(2020, 2, 20)
    utc_time = local_time - datetime.timedelta(seconds=time.timezone)
    expected_timestamp = time.mktime(utc_time.timetuple())

    freezer.start()
    assert time.time() == expected_timestamp
    assert datetime.datetime.now() == datetime.datetime(2020, 2, 20)
    assert datetime.datetime.utcnow() == datetime.datetime(2020, 2, 20)
    assert datetime.date.today() == datetime.date(2020, 2, 20)
    freezer.stop()
    assert time.time() != expected_timestamp
    assert datetime.datetime.now() != datetime.datetime(2020, 2, 20)
    assert datetime.datetime.utcnow() != datetime.datetime(2020, 2, 20)

    freezer = freeze_time("2020-02-15 08:30:10")
    freezer.start()
    assert datetime.datetime.now() == datetime.datetime(2020, 2, 15, 8, 30, 10)
    freezer.stop()


def test_public_tz_offset() -> None:
    freezer = freeze_time("2020-03-05 05:45:00", tz_offset=-5)
    local_time = datetime.datetime(2020, 3, 5, 5, 45, 0)
    utc_time = local_time - datetime.timedelta(seconds=time.timezone)
    expected_timestamp = time.mktime(utc_time.timetuple())
    freezer.start()
    assert datetime.datetime.now() == datetime.datetime(2020, 3, 5 - 1, 0, 45, 0) or datetime.datetime.now() == datetime.datetime(2020, 3, 4, 0, 45, 0)
    assert datetime.datetime.utcnow() == datetime.datetime(2020, 3, 5, 5, 45, 0)
    assert time.time() == expected_timestamp
    freezer.stop()


def test_public_tz_offset_today() -> None:
    freezer = freeze_time("2021-12-11", tz_offset=-3)
    freezer.start()
    assert datetime.date.today() == datetime.date(2021, 12, 10)
    freezer.stop()
    assert datetime.date.today() != datetime.date(2021, 12, 10)


def test_public_zero_tz_offset_with_time() -> None:
    freezer = freeze_time('1960-01-01')
    freezer.start()
    assert datetime.date.today() == datetime.date(1960, 1, 1)
    assert datetime.datetime.now() == datetime.datetime(1960, 1, 1)
    assert datetime.datetime.utcnow() == datetime.datetime(1960, 1, 1)
    # The expected time.time() is -315619200.0 based on the difference from 1970-01-01
    assert int(time.time()) == -315619200
    freezer.stop()