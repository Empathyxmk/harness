import json

class LngLatAlt:
    def __init__(self, lon, lat, alt):
        self.lon = lon
        self.lat = lat
        self.alt = alt

    def __eq__(self, other):
        return (
            isinstance(other, LngLatAlt) and
            abs(self.lon - other.lon) < 1e-9 and
            abs(self.lat - other.lat) < 1e-9 and
            abs(self.alt - other.alt) < 1e-9
        )

def test_serialization():
    pos = LngLatAlt(49.43245, 52.42345, 120.34626)
    correct_json = '[49.43245,52.42345,120.34626]'
    produced_json = json.dumps([pos.lon, pos.lat, pos.alt])
    assert produced_json == correct_json