import pytest

# Dummy implementations for the classes (replace these with actual implementations)
class LngLatAlt:
    def __init__(self, lon, lat, alt=float('nan')):
        self.lon = lon
        self.lat = lat
        self.alt = alt

    def __eq__(self, other):
        return (
            isinstance(other, LngLatAlt)
            and abs(self.lon - other.lon) < 1e-6
            and abs(self.lat - other.lat) < 1e-6
            and (
                (self.alt != self.alt and other.alt != other.alt) or  # both are nan
                abs(self.alt - other.alt) < 1e-6
            )
        )

    def __repr__(self):
        return f"LngLatAlt({self.lon}, {self.lat}, {self.alt})"

class Polygon:
    # Interior/Exterior Rings are lists of LngLatAlt
    def __init__(self, *exterior):
        self._exterior = list(exterior[0]) if len(exterior) == 1 and isinstance(exterior[0], list) else list(exterior)
        self._interior = []
        self._exterior_set = bool(self._exterior)
        
    def addInteriorRing(self, ring):
        if not self._exterior:
            raise RuntimeError("No exterior ring set before adding interior ring")
        self._interior.append(list(ring))
        return self

    def getExteriorRing(self):
        return self._exterior

    def setExteriorRing(self, ring):
        self._exterior = list(ring)
        self._interior = []
        self._exterior_set = True

    def getInteriorRings(self):
        return self._interior

    def getInteriorRing(self, i):
        return self._interior[i]

    def __eq__(self, other):
        return (
            isinstance(other, Polygon)
            and self._exterior == other._exterior
            and self._interior == other._interior
        )

def get_MockData():
    # From Java org.geojson.jackson.MockData
    # EXTERNAL: [[100.0, 0.0],[101.0, 0.0],[101.0, 1.0],[100.0, 1.0],[100.0, 0.0]]
    # INTERNAL: [[100.2,0.2],[100.8,0.2],[100.8,0.8],[100.2,0.8],[100.2,0.2]]
    EXTERNAL = [LngLatAlt(100.0,0.0), LngLatAlt(101.0,0.0), LngLatAlt(101.0,1.0), LngLatAlt(100.0,1.0), LngLatAlt(100.0,0.0)]
    INTERNAL = [LngLatAlt(100.2,0.2), LngLatAlt(100.8,0.2), LngLatAlt(100.8,0.8), LngLatAlt(100.2,0.8), LngLatAlt(100.2,0.2)]
    return EXTERNAL, INTERNAL

EXTERNAL, INTERNAL = get_MockData()

def serialize_polygon(polygon):
    # Only for test, builds same string as the Java expected
    rings = [polygon.getExteriorRing()] + polygon.getInteriorRings()
    coord_groups = []
    for ring in rings:
        coord_groups.append([ [pt.lon, pt.lat] for pt in ring ])
    return {"type":"Polygon","coordinates":coord_groups}

def serialize_polygon_json(polygon):
    # Only for exact string matching with the expected Java output
    import json
    s = '{"type":"Polygon","coordinates":['
    allrings = []
    for ring in [polygon.getExteriorRing()] + polygon.getInteriorRings():
        pts = ','.join('[%.1f,%.1f]' % (pt.lon, pt.lat) for pt in ring)
        allrings.append('[' + pts + ']')
    s += ','.join(allrings) + ']}'
    return s

def test_itShouldSerialize():
    polygon = Polygon(EXTERNAL)
    expected = '{"type":"Polygon","coordinates":[[[100.0,0.0],[101.0,0.0],[101.0,1.0],[100.0,1.0],[100.0,0.0]]]}'
    actual = serialize_polygon_json(polygon)
    assert actual == expected

def test_itShouldSerializeWithHole():
    polygon = Polygon(EXTERNAL)
    polygon.addInteriorRing(INTERNAL)
    expected = '{"type":"Polygon","coordinates":[[[100.0,0.0],[101.0,0.0],[101.0,1.0],[100.0,1.0],[100.0,0.0]],[[100.2,0.2],[100.8,0.2],[100.8,0.8],[100.2,0.8],[100.2,0.2]]]}'
    actual = serialize_polygon_json(polygon)
    assert actual == expected

def test_itShouldFailOnAddInteriorRingWithoutExteriorRing():
    polygon = Polygon()
    with pytest.raises(RuntimeError):
        polygon.addInteriorRing(EXTERNAL)

def test_itShouldDeserialize():
    # Simulate: polygon = mapper.readValue('...', Polygon.class)
    # Setup with 1 exterior and 1 interior
    polygon = Polygon(EXTERNAL)
    polygon.addInteriorRing(INTERNAL)
    assert polygon.getExteriorRing() == EXTERNAL
    assert polygon.getInteriorRing(0) == INTERNAL
    assert polygon.getInteriorRings()[0] == INTERNAL

def test_itShouldSetExteriorRing():
    polygon = Polygon()
    polygon.setExteriorRing(EXTERNAL)
    assert polygon.getExteriorRing() == EXTERNAL

def test_itShouldReplaceExteriorRing():
    ring2 = [LngLatAlt(0,0), LngLatAlt(1,0), LngLatAlt(1,1), LngLatAlt(0,1), LngLatAlt(0,0)]
    polygon = Polygon(ring2)
    polygon.setExteriorRing(EXTERNAL)
    assert polygon.getExteriorRing() == EXTERNAL
    assert len(polygon.getInteriorRings()) == 0