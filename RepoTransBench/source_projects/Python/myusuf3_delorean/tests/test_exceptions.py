import pytest
from delorean.exceptions import DeloreanError, DeloreanInvalidTimezone, DeloreanInvalidDatetime

def test_delorean_error_str():
    e = DeloreanError("msg!")
    assert str(e) == "msg!"
    assert isinstance(e, Exception)

def test_delorean_invalid_timezone_is_subclass():
    e = DeloreanInvalidTimezone("bad tz")
    assert str(e) == "bad tz"
    assert isinstance(e, DeloreanError)

def test_delorean_invalid_datetime_is_subclass():
    e = DeloreanInvalidDatetime("bad dt")
    assert str(e) == "bad dt"
    assert isinstance(e, DeloreanError)