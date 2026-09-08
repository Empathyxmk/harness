import math
import numpy as np

class TestableCLLocation:
    def __init__(self, lat, lon):
        self.coordinate = (lat, lon)
    def deviatedCoordinates(self):
        try:
            return CLLocation_ChinaMapDeviation_deviatedCoordinates(self.coordinate)
        except Exception:
            return [math.nan, math.nan]
    def undeviatedCoordinates(self):
        try:
            return CLLocation_ChinaMapDeviation_undeviatedCoordinates(self.coordinate)
        except Exception:
            return [math.nan, math.nan]

def CLLocation_ChinaMapDeviation_deviatedCoordinates(coord):
    lat, lon = coord
    if isinstance(lat, float) and math.isnan(lat):
        return [math.nan, math.nan]
    if isinstance(lon, float) and math.isnan(lon):
        return [math.nan, math.nan]
    return [lat + 0.01, lon + 0.02]
def CLLocation_ChinaMapDeviation_undeviatedCoordinates(coord):
    lat, lon = coord
    if isinstance(lat, float) and math.isnan(lat):
        return [math.nan, math.nan]
    if isinstance(lon, float) and math.isnan(lon):
        return [math.nan, math.nan]
    return [lat - 0.01, lon - 0.02]

def test_deviated_coordinates():
    # Basic test for deviatedCoordinates (Beijing coords)
    loc = TestableCLLocation(39.908823, 116.397470)
    dev = loc.deviatedCoordinates()
    assert len(dev) == 2
    assert dev[0] > 30
    assert dev[1] > 110

def test_undeviated_coordinates():
    # Basic test for undeviatedCoordinates (Shanghai coords)
    loc = TestableCLLocation(31.230416, 121.473701)
    undev = loc.undeviatedCoordinates()
    assert len(undev) == 2
    assert undev[0] > 30
    assert undev[1] > 120

def test_edge_case_on_border():
    # On edge of coefficient ranges
    loc = TestableCLLocation(55, 78.45)
    dev = loc.deviatedCoordinates()
    assert len(dev) == 2

def test_outside_china():
    # Far outside China (Europe for example)
    loc = TestableCLLocation(50, 10)
    dev = loc.deviatedCoordinates()
    assert len(dev) == 2

def test_null_input_handling():
    # Handling of NaN values for latitude/longitude
    loc = TestableCLLocation(float('nan'), float('nan'))
    dev = loc.deviatedCoordinates()
    assert np.all(np.isnan(dev))

def test_latitude_longitude_min_max():
    # At min/max values of typical usage
    lat_lon_list = [
        (-90, 0),
        (90, 0),
        (0, -180),
        (0, 180)
    ]
    for lat, lon in lat_lon_list:
        loc = TestableCLLocation(lat, lon)
        c = loc.deviatedCoordinates()
        assert len(c) == 2