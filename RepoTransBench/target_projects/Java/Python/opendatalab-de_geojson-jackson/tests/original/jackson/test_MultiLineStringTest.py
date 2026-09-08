class LngLatAlt:
    def __init__(self, lon, lat):
        self.lon = lon
        self.lat = lat

    def __eq__(self, other):
        return isinstance(other, LngLatAlt) and abs(self.lon - other.lon) < 1e-6 and abs(self.lat - other.lat) < 1e-6

    def __repr__(self):
        return f"LngLatAlt({self.lon}, {self.lat})"

class MultiLineString:
    def __init__(self):
        self.lines = []

    def add(self, points):
        self.lines.append(list(points))
        return self

def test_itShouldSerialize():
    multiLineString = MultiLineString()
    multiLineString.add([LngLatAlt(100, 0), LngLatAlt(101, 1)])
    multiLineString.add([LngLatAlt(102, 2), LngLatAlt(103, 3)])
    expected = '{"type":"MultiLineString","coordinates":[[[100.0,0.0],[101.0,1.0]],[[102.0,2.0],[103.0,3.0]]]}'
    # Compose JSON string to match expected
    def to_json_str(mls):
        group_strs = []
        for line in mls.lines:
            group_strs.append('[' + ','.join(f'[{pt.lon},{pt.lat}]' for pt in line) + ']')
        return '{"type":"MultiLineString","coordinates":[' + ','.join(group_strs) + ']}'
    actual = to_json_str(multiLineString)
    assert actual == expected