import pytest
from src.ctime import ctime_format_seconds, ctime_format_millis

def test_format_seconds():
    assert ctime_format_seconds(5) == "5.00s"
    assert ctime_format_seconds(70) == "1m10s"
    assert ctime_format_seconds(7542) == "2h5m42s"

def test_format_millis():
    assert ctime_format_millis(123) == "123ms"
    assert ctime_format_millis(1245) == "1s245ms"
    assert ctime_format_millis(65599) == "1m5s599ms"