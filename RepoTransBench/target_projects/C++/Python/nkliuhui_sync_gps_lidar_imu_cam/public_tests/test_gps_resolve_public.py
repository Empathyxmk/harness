import pytest
from src.gps_driver.gps_resolve_object import GPSResolveObject

def test_parse_gga_with_different_data():
    gpsObj = GPSResolveObject()
    gga = "$GPGGA,094525.000,4045.0000,N,07358.0000,W,2,12,1.0,15.3,M,-34.0,M,,*68"
    assert gpsObj.Resolve(gga)
    assert gpsObj.Latitude == (40 + 45.0000 / 60)
    assert gpsObj.Longitude == -(73 + 58.0000 / 60)
    assert gpsObj.FixQuality == 2
    assert gpsObj.NumSatellites == 12
    assert gpsObj.HDOP == 1.0
    assert gpsObj.Altitude == 15.3

def test_parse_gga_minimal_satellites():
    gpsObj = GPSResolveObject()
    gga = "$GPGGA,032101.000,2230.2500,S,11330.3000,E,1,01,0.8,-2.0,M,8.0,M,,*70"
    assert gpsObj.Resolve(gga)
    assert gpsObj.Latitude == -(22 + 30.2500 / 60)
    assert gpsObj.Longitude == (113 + 30.3000 / 60)
    assert gpsObj.FixQuality == 1
    assert gpsObj.NumSatellites == 1
    assert gpsObj.HDOP == 0.8
    assert gpsObj.Altitude == -2.0

def test_parse_invalid_sentences():
    gpsObj = GPSResolveObject()
    gga = "$GPGGA,235959.000,,,,,,0,00,99.99,,M,0.0,M,,*48"
    assert not gpsObj.Resolve(gga)

    gll = "$GPGLL,4916.45,N,12311.12,W,225444,A,*1D"
    assert not gpsObj.Resolve(gll)
    
    assert not gpsObj.Resolve("XYZ, no commas")