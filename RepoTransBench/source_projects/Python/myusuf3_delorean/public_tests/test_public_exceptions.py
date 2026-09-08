import pytest
from delorean.exceptions import DeloreanError, DeloreanInvalidTimezone, DeloreanInvalidDatetime

def test_delorean_error_str_public():
    e = DeloreanError("public error!")
    assert str(e) == "public error!"
    assert isinstance(e, Exception)

def test_delorean_invalid_timezone_is_subclass_public():
    e = DeloreanInvalidTimezone("public bad tz")
    assert str(e) == "public bad tz"
    assert isinstance(e, DeloreanError)

def test_delorean_invalid_datetime_is_subclass_public():
    e = DeloreanInvalidDatetime("public bad dt")
    assert str(e) == "public bad dt"
    assert isinstance(e, DeloreanError)