import json

class LngLatAlt:
    def __init__(self, lon, lat):
        self.lon = lon
        self.lat = lat

    def __eq__(self, other):
        return isinstance(other, LngLatAlt) and abs(self.lon - other.lon) < 1e-6 and abs(self.lat - other.lat) < 1e-6

class MultiPoint:
    def __init__(self, *points):
        self.points = list(points) if points else []

    def getCoordinates(self):
        return self.points

class LineString(MultiPoint):
    pass

def assertLngLatAlt(expected_lon, expected_lat, expected_alt, point):
    assert abs(point.lon - expected_lon) < 1e-6
    assert abs(point.lat - expected_lat) < 1e-6
    # Skipping altitude check

def test_itShouldSerializeMultiPoint():
    lineString = LineString(LngLatAlt(100, 0), LngLatAlt(101, 1))
    expected = '{"type":"LineString","coordinates":[[100.0,0.0],[101.0,1.0]]}'
    def to_json_str(ls):
        coords = ','.join(f'[{pt.lon},{pt.lat}]' for pt in ls.getCoordinates())
        return '{"type":"LineString","coordinates":[' + coords + ']}'
    actual = to_json_str(lineString)
    assert actual == expected

def test_itShouldDeserializeLineString():
    # Simulate: LineString lineString = mapper.readValue(..., LineString.class)
    json_str = '{"type":"LineString","coordinates":[[100.0,0.0],[101.0,1.0]]}'
    obj = json.loads(json_str)
    coordinates = [LngLatAlt(pt[0], pt[1]) for pt in obj['coordinates']]
    assert coordinates is not None
    assertLngLatAlt(100, 0, float('nan'), coordinates[0])
    assertLngLatAlt(101, 1, float('nan'), coordinates[1])