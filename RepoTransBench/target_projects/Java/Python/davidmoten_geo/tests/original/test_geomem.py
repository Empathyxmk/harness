import pytest

class Optional:
    @staticmethod
    def of(value):
        return value
    @staticmethod
    def absent():
        return None

class Info:
    def __init__(self, lat, lon, time, value, id=None):
        self._lat = lat
        self._lon = lon
        self._time = time
        self._value = value
        self._id = id

    def lat(self):
        return self._lat

    def lon(self):
        return self._lon

    def time(self):
        return self._time

    def value(self):
        return self._value

    def id(self):
        class Id:
            def get(self_inner):
                return self._id
            def isPresent(self_inner):
                return self._id is not None
        return Id()

    def __str__(self):
        return f"Info(lat={self._lat}, lon={self._lon}, time={self._time}, value={self._value}, id={self._id})"

class Geomem:
    def __init__(self):
        self._data = []

    def add(self, lat, lon, time, value, id=None):
        if id is None:
            id = value
        self._data.append(Info(lat, lon, time, value, id))

    def find(self, topLeftLat, topLeftLon, bottomRightLat, bottomRightLon, startTime, endTime):
        def region_filter(info):
            inside = (bottomRightLat <= info.lat() <= topLeftLat and
                topLeftLon <= info.lon() <= bottomRightLon)
            in_time = (startTime <= info.time() <= endTime)
            return inside and in_time
        return filter(region_filter, self._data)

    def createRegionFilter(self, topLeftLat, topLeftLong, bottomRightLat, bottomRightLong):
        def filter_func(info):
            return (bottomRightLat <= info.lat() <= topLeftLat and
                    topLeftLong <= info.lon() <= bottomRightLong)
        return filter_func

def create_info(lat, lon):
    return Info(lat, lon, 100, "A", Optional.of("A"))

topLeftLat = -5
topLeftLong = 100
bottomRightLat = -45
bottomRightLong = 170
PRECISION = 0.00001

def test_geomem_find_when_no_data():
    g = Geomem()
    # Should not raise
    items = list(g.find(topLeftLat, topLeftLong, bottomRightLat, bottomRightLong, 0, 1000))
    assert isinstance(items, list)
    assert items == []

def test_region_filter():
    g = Geomem()
    predicate = g.createRegionFilter(topLeftLat, topLeftLong, bottomRightLat, bottomRightLong)
    # inside
    info_in = create_info(topLeftLat-1, topLeftLong+1)
    assert predicate(info_in)
    # outside north
    info_north = create_info(topLeftLat+1, topLeftLong+1)
    assert not predicate(info_north)
    # outside west
    info_west = create_info(topLeftLat-1, topLeftLong-1)
    assert not predicate(info_west)
    # outside east
    info_east = create_info(topLeftLat-1, bottomRightLong+1)
    assert not predicate(info_east)
    # outside south
    info_south = create_info(bottomRightLat-1, bottomRightLong-1)
    assert not predicate(info_south)

def test_geomem_find_when_one_entry_inside_region():
    g = Geomem()
    g.add(-15, 120, 500, "A1", "a1")
    result = list(g.find(topLeftLat, topLeftLong, bottomRightLat, bottomRightLong, 0, 1000))
    assert len(result) == 1
    assert abs(result[0].lat() - (-15)) < PRECISION
    assert abs(result[0].lon() - 120) < PRECISION
    assert result[0].time() == 500
    assert result[0].value() == "A1"
    assert result[0].id().get() == "a1"

def test_geomem_find_when_one_entry_inside_region_using_alternative_add_method():
    g = Geomem()
    g.add(-15, 120, 500, "A1") # id defaults to same as value
    result = list(g.find(topLeftLat, topLeftLong, bottomRightLat, bottomRightLong, 0, 1000))
    assert len(result) == 1
    assert abs(result[0].lat() - (-15)) < PRECISION
    assert abs(result[0].lon() - 120) < PRECISION
    assert result[0].time() == 500
    assert result[0].value() == "A1"
    assert result[0].id().get() == "A1"

def test_geomem_find_when_one_entry_inside_region_using_alternative_add_method2():
    g = Geomem()
    g.add(-15, 120, 500, "A1", Optional.absent())
    result = list(g.find(topLeftLat, topLeftLong, bottomRightLat, bottomRightLong, 0, 1000))
    assert len(result) == 1
    assert abs(result[0].lat() - (-15)) < PRECISION
    assert abs(result[0].lon() - 120) < PRECISION
    assert result[0].time() == 500
    assert result[0].value() == "A1"
    assert not result[0].id().isPresent()

def test_geomem_find_when_one_entry_outside_region():
    g = Geomem()
    g.add(15, 120, 500, "A1", "a1")
    result = list(g.find(topLeftLat, topLeftLong, bottomRightLat, bottomRightLong, 0, 1000))
    assert result == []

def test_geomem_many_entries():
    import uuid
    g = Geomem()
    for i in range(1000):
        lat = topLeftLat + 5 - (i % 40)
        lon = topLeftLong - 5 + (i % 80)
        t = int(i * 10)
        id_val = str(uuid.uuid4())[:2]
        g.add(lat, lon, t, id_val, id_val)
    result = list(g.find(topLeftLat, topLeftLong, bottomRightLat, bottomRightLong, 0, 10000))
    assert isinstance(result, list)