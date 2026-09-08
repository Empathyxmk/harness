import json

class LngLatAlt:
    def __init__(self, lon, lat):
        self.lon = lon
        self.lat = lat

    def __eq__(self, other):
        return isinstance(other, LngLatAlt) and abs(self.lon - other.lon) < 1e-6 and abs(self.lat - other.lat) < 1e-6
    
    def __repr__(self):
        return f"LngLatAlt({self.lon}, {self.lat})"

def get_MockData():
    # EXTERNAL: [[100.0, 0.0],[101.0, 0.0],[101.0, 1.0],[100.0, 1.0],[100.0, 0.0]]
    # INTERNAL: [[100.2,0.2],[100.8,0.2],[100.8,0.8],[100.2,0.8],[100.2,0.2]]
    EXTERNAL = [LngLatAlt(100.0,0.0), LngLatAlt(101.0,0.0), LngLatAlt(101.0,1.0), LngLatAlt(100.0,1.0), LngLatAlt(100.0,0.0)]
    INTERNAL = [LngLatAlt(100.2,0.2), LngLatAlt(100.8,0.2), LngLatAlt(100.8,0.8), LngLatAlt(100.2,0.8), LngLatAlt(100.2,0.2)]
    return EXTERNAL, INTERNAL

EXTERNAL, INTERNAL = get_MockData()

class Polygon:
    def __init__(self, *rings):
        self.rings = []
        if len(rings)==1 and isinstance(rings[0], list):
            self.rings.append(list(rings[0]))
        elif rings:
            self.rings.append(list(rings))
        self.interior = []
    def addInteriorRing(self, ring):
        self.interior.append(list(ring))
        return self

    def getCoordinates(self):
        return [self.rings[0]] + self.interior if self.rings else []

class MultiPolygon:
    def __init__(self):
        self.coords = []
    def add(self, x):
        self.coords.append([list(x)])
    def getCoordinates(self):
        return self.coords

def test_itShouldSerialize():
    multiPolygon = MultiPolygon()
    multiPolygon.add(Polygon([LngLatAlt(102, 2), LngLatAlt(103, 2), LngLatAlt(103, 3), LngLatAlt(102, 3), LngLatAlt(102, 2)]).getCoordinates()[0])
    polygon = Polygon(EXTERNAL)
    polygon.addInteriorRing(INTERNAL)
    multiPolygon.add(polygon.getCoordinates())
    # reconstruct into serialized json (as string, with inner rings per Java)
    expected = '{"type":"MultiPolygon","coordinates":[[[[102.0,2.0],[103.0,2.0],[103.0,3.0],[102.0,3.0],[102.0,2.0]]],[[[100.0,0.0],[101.0,0.0],[101.0,1.0],[100.0,1.0],[100.0,0.0]],[[100.2,0.2],[100.8,0.2],[100.8,0.8],[100.2,0.8],[100.2,0.2]]]]}'
    # generate string
    rings_str = []
    for polygon_list in multiPolygon.getCoordinates():
        rings_inner = []
        for ring in polygon_list:
            pts = ','.join(f'[{pt.lon},{pt.lat}]' for pt in ring)
            rings_inner.append(f'[{pts}]')
        rings_str.append('[' + ','.join(rings_inner) + ']')
    actual = '{"type":"MultiPolygon","coordinates":[' + ','.join(rings_str) + ']}'
    assert actual == expected

def test_itShouldDeserialize():
    # Build equivalent to:
    # MultiPolygon multiPolygon = mapper.readValue(..., MultiPolygon.class);
    # assertEquals(2, multiPolygon.getCoordinates().size());
    class MultiPolygonDeserializer:
        @staticmethod
        def from_json(json_str):
            obj = json.loads(json_str)
            result = []
            for polygon in obj['coordinates']:
                ringlist = []
                for ring in polygon:
                    ringlist.append([LngLatAlt(pt[0], pt[1]) for pt in ring])
                result.append(ringlist)
            return result

    json_str = '{"type":"MultiPolygon","coordinates":[[[[102.0,2.0],[103.0,2.0],[103.0,3.0],[102.0,3.0],[102.0,2.0]]],[[[100.0,0.0],[101.0,0.0],[101.0,1.0],[100.0,1.0],[100.0,0.0]],[[100.2,0.2],[100.8,0.2],[100.8,0.8],[100.2,0.8],[100.2,0.2]]]]}'
    coords = MultiPolygonDeserializer.from_json(json_str)
    assert len(coords) == 2