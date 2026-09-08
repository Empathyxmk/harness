import pytest

class LatLong:
    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon

    def __eq__(self, other):
        if not isinstance(other, LatLong):
            return False
        return self.lat == other.lat and self.lon == other.lon

    def __hash__(self):
        return hash((self.lat, self.lon))

    def __str__(self):
        return f"LatLong [lat={self.lat}, lon={self.lon}]"

    def getLat(self):
        return self.lat

    def getLon(self):
        return self.lon

def test_to_string():
    ll = LatLong(10, 20)
    assert str(ll) == "LatLong [lat=10, lon=20]"

def test_hash_code():
    lat = 20.05
    lon = -15.5
    a = LatLong(lat, lon)
    b = LatLong(lat, lon)
    assert hash(a) == hash(b)
    assert a == b