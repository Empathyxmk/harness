class LatLong:
    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon

    def getLat(self):
        return self.lat

    def getLon(self):
        return self.lon

def test_lat_long_values():
    ll = LatLong(12.3, 45.6)
    assert ll.getLat() == 12.3
    assert ll.getLon() == 45.6