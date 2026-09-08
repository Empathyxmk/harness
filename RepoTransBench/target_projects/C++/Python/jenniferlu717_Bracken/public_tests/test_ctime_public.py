import pytest
from src.ctime import ctime_format_seconds, ctime_format_millis

def test_format_seconds_public():
    assert ctime_format_seconds(9) == "9.00s"
    assert ctime_format_seconds(125) == "2m5s"
    assert ctime_format_seconds(7261) == "2h1m1s"

def test_format_millis_public():
    assert ctime_format_millis(999) == "999ms"
    assert ctime_format_millis(2156) == "2s156ms"
    assert ctime_format_millis(134567) == "2m14s567ms"