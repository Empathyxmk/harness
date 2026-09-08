import re
import pytest
from pytimeparse import timeparse

def test_public_MINCLOCK_regex():
    MINCLOCK = re.compile(r'^([+-]?)(\d{1,2}):(\d{2})$')
    m = MINCLOCK.match("11:25")
    assert m is not None
    assert m.group(2) == "11"
    assert m.group(3) == "25"
    # Diff input
    m2 = MINCLOCK.match("+05:09")
    assert m2 is not None
    assert m2.group(1) == "+"
    assert m2.group(2) == "05"
    assert m2.group(3) == "09"
    # Negative
    m3 = MINCLOCK.match("-10:10")
    assert m3.group(1) == "-"

def test_public_HOURMINSEC_regex():
    HOURMINSEC = re.compile(r'^([+-]?\d+):([0-5]?\d):([0-5]?\d(?:\.\d*)?)$')
    m = HOURMINSEC.match("12:44:55")
    assert m is not None
    assert m.group(1) == "12"
    assert m.group(2) == "44"
    assert m.group(3) == "55"
    m2 = HOURMINSEC.match("-2:00:05.5")
    assert m2.group(1) == "-2"
    assert m2.group(3) == "05.5"

def test_public_keyword_sec_min_hour():
    assert timeparse.timeparse("7 hours") == 25200
    assert timeparse.timeparse("15min") == 900
    assert timeparse.timeparse("21.5 sec") == pytest.approx(21.5)
    assert timeparse.timeparse("0h") == None
    assert timeparse.timeparse("0m") == None
    assert timeparse.timeparse("0s") == None

def test_public_other_patterns():
    # Just hours and mins as float
    assert timeparse.timeparse("2.75h") == 2.75 * 3600
    assert timeparse.timeparse("7.5m") == 7.5 * 60
    assert timeparse.timeparse("21.5s") == pytest.approx(21.5)
    assert timeparse.timeparse("-21.5s") == pytest.approx(-21.5)
    # Weeks and days
    assert timeparse.timeparse("1w") == 604800
    assert timeparse.timeparse("2d") == 172800