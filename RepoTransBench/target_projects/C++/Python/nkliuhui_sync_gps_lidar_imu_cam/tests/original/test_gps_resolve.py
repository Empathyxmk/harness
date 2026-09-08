import pytest
from src.gps_driver.gps_resolve import GPSData, parse_gps_sentence, gps_data_to_string

def test_parse_valid_sentence():
    d = GPSData()
    result = parse_gps_sentence("$GPGGA,34.0,120.1,1", d)
    assert result
    assert d.latitude == 34.0
    assert d.longitude == 120.1
    assert d.fix_ok

def test_parse_invalid_sentence_type():
    d = GPSData()
    result = parse_gps_sentence("$GPVTG,34.0,120.1,1", d)
    assert not result

def test_parse_empty_sentence():
    d = GPSData()
    result = parse_gps_sentence("", d)
    assert not result

def test_parse_no_fix():
    d = GPSData()
    result = parse_gps_sentence("$GPGGA,20.0,32.0,0", d)
    assert result
    assert d.latitude == 20.0
    assert d.longitude == 32.0
    assert not d.fix_ok

def test_to_string():
    d = GPSData(55.2, 44.1, True)
    s = gps_data_to_string(d)
    assert "Lat:55.20000,Lon:44.10000,Fix:1" in s