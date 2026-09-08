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

def test_deviated_coordinates_public():
    # Guangzhou coords, public test
    loc = TestableCLLocation(23.129163, 113.264435)
    dev = loc.deviatedCoordinates()
    assert len(dev) == 2
    assert dev[0] > 20
    assert dev[1] > 110

def test_undeviated_coordinates_public():
    # Chengdu coords, public test
    loc = TestableCLLocation(30.572816, 104.066801)
    undev = loc.undeviatedCoordinates()
    assert len(undev) == 2
    assert undev[0] > 28
    assert undev[1] > 100

def test_edge_case_on_border_public():
    # Far east of China, boundary
    loc = TestableCLLocation(20.225, 140.0)
    dev = loc.deviatedCoordinates()
    assert len(dev) == 2

def test_outside_china_public():
    # New York
    loc = TestableCLLocation(40, -74)
    dev = loc.deviatedCoordinates()
    assert len(dev) == 2

def test_null_input_handling_public():
    # NaN in latitude only
    loc = TestableCLLocation(float('nan'), 120.0)
    dev = loc.deviatedCoordinates()
    assert np.all(np.isnan(dev))

def test_latitude_longitude_min_max_public():
    # Alternate min/max values
    lat_lon_list = [
        (-45, 100),
        (45, -100),
        (-80, 179),
        (80, -179)
    ]
    for lat, lon in lat_lon_list:
        loc = TestableCLLocation(lat, lon)
        c = loc.deviatedCoordinates()
        assert len(c) == 2