class Info:
    def __init__(self, lat, lon, time, value):
        self._lat = lat
        self._lon = lon
        self._time = time
        self._value = value

    def lat(self):
        return self._lat

    def lon(self):
        return self._lon

    def time(self):
        return self._time

    def value(self):
        return self._value

def test_info_fields():
    ii = Info(1, 2, 3, "A")
    assert ii.lat() == 1
    assert ii.lon() == 2
    assert ii.time() == 3
    assert ii.value() == "A"