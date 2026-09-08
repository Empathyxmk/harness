import pytest

def ID(x):
    return x

# Python stub for semi.static_map matching public test pattern.
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

class StaticMapStrStr(metaclass=StaticMapMeta):
    @classmethod
    def default_value(cls): return ""

def test_static_map_public():
    # Compile-time only load/store
    class Tag: pass
    Map = StaticMapStrStr
    StaticMapMeta._data.pop(Map, None)
    animal = Map.get(ID("animal"))
    assert animal == ""
    Map.get(ID("animal"))
    Map._data[Map][ID("animal")] = "cat"
    assert Map.get(ID("animal")) == "cat"
    color = Map.get(ID("color"))
    assert color == ""
    Map._data[Map][ID("color")] = "red"
    assert Map.get(ID("animal")) == "cat"
    assert Map.get(ID("color")) == "red"
    Map._data[Map][ID("animal")] = "dog"
    assert Map.get(ID("animal")) == "dog"
    assert Map.get(ID("color")) == "red"
    Map._data[Map][ID("color")] = "blue"
    assert Map.get(ID("animal")) == "dog"
    assert Map.get(ID("color")) == "blue"
    assert Map.get(ID("fruit"), "apple") == "apple"
    assert Map.get(ID("fruit"), "banana") == "apple"

    # Runtime load/store
    StaticMapMeta._data.pop(Map, None)
    animal = Map.get("animal")
    assert animal == ""
    Map._data[Map]["animal"] = "cat"
    assert Map.get("animal") == "cat"
    color = Map.get("color")
    assert color == ""
    Map._data[Map]["color"] = "red"
    assert Map.get("animal") == "cat"
    assert Map.get("color") == "red"
    Map._data[Map]["animal"] = "dog"
    assert Map.get("animal") == "dog"
    assert Map.get("color") == "red"
    Map._data[Map]["color"] = "blue"
    assert Map.get("animal") == "dog"
    assert Map.get("color") == "blue"
    assert Map.get("fruit", "apple") == "apple"
    assert Map.get("fruit", "banana") == "apple"

    # Mixed
    StaticMapMeta._data.pop(Map, None)
    Map._data[Map][ID("animal")] = "cat"
    assert Map.get("animal") == "cat"
    Map._data[Map]["color"] = "red"
    assert Map.get(ID("color")) == "red"
    assert Map.get(ID("animal")) == "cat"
    assert Map.get("color") == "red"
    assert Map.get(ID("fruit"), "apple") == "apple"
    assert Map.get("fruit", "banana") == "apple"
    assert Map.get("snack", "chips") == "chips"
    assert Map.get(ID("snack"), "crackers") == "chips"

    # clear & contains
    StaticMapMeta._data.pop(Map, None)
    assert not Map.contains(ID("animal"))
    assert not Map.contains("animal")
    assert not Map.contains(ID("animal"))
    assert not Map.contains("animal")
    Map._data[Map][ID("animal")] = "cat"
    assert Map.contains(ID("animal"))
    assert Map.contains("animal")
    assert not Map.contains(ID("color"))
    assert not Map.contains("color")
    Map.clear()
    assert not Map.contains(ID("animal"))
    assert not Map.contains("animal")
    Map._data[Map]["color"] = "red"
    assert Map.contains("color")
    assert Map.contains(ID("color"))
    assert not Map.contains("animal")
    assert not Map.contains(ID("animal"))
    Map.clear()
    assert not Map.contains("color")
    assert not Map.contains(ID("color"))