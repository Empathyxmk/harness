import pytest

def ID(x):
    return x

class StaticMapMeta(type):
    _data = {}
    def get(cls, key, fallback=None):
        dct = StaticMapMeta._data.setdefault(cls, {})
        if fallback is not None:
            if key not in dct:
                dct[key] = fallback
            return dct[key]
        if key not in dct:
            dct[key] = cls.default_value()
        return dct[key]
    def clear(cls):
        dct = StaticMapMeta._data.setdefault(cls, {})
        dct.clear()
    def contains(cls, key):
        dct = StaticMapMeta._data.setdefault(cls, {})
        return key in dct

class StaticMapStrInt(metaclass=StaticMapMeta):
    @classmethod
    def default_value(cls): return 0
class StaticMapStrStr(metaclass=StaticMapMeta):
    @classmethod
    def default_value(cls): return ""
class StaticMapIntVectorInt(metaclass=StaticMapMeta):
    @classmethod
    def default_value(cls): return []

def test_static_map_types_pub():
    # Numeric type and different keys
    class Tag: pass
    Map = StaticMapStrInt
    StaticMapMeta._data.pop(Map, None)
    assert not Map.contains(ID("year"))
    Map._data[Map][ID("year")] = 2024
    assert Map.contains(ID("year"))
    assert Map.get("year") == 2024
    Map._data[Map]["month"] = 6
    assert Map.get(ID("month")) == 6
    assert Map.get(ID("day"), 15) == 15
    assert Map.get("day", 23) == 15
    Map.clear()
    assert not Map.contains("year")
    assert not Map.contains(ID("month"))

    # Non-str keys/values: int, list (vector)
    class Tag2: pass
    Map = StaticMapIntVectorInt
    StaticMapMeta._data.pop(Map, None)
    assert not Map.contains(ID(10))
    Map._data[Map][ID(10)] = [21, 22]
    assert len(Map.get(ID(10))) == 2
    assert Map.get(20) == []
    Map._data[Map][20] = [33]
    assert len(Map.get(ID(20))) == 1
    Map._data[Map][20].append(44)
    assert len(Map.get(ID(20))) == 2
    assert len(Map.get(ID(30), [5, 7, 9])) == 3

def test_static_map_edge_cases_pub():
    class Tag: pass
    Map = StaticMapStrStr
    StaticMapMeta._data.pop(Map, None)
    assert not Map.contains(ID("zzz"))
    Map._data[Map][ID("zzz")] = ""
    assert Map.contains(ID("zzz"))
    assert Map.get("zzz") == ""
    Map._data[Map]["zzz"] = "xyz"
    assert Map.get(ID("zzz")) == "xyz"
    Map.clear()
    assert not Map.contains(ID("zzz"))