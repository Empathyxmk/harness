import pytest

# ======== Python semi.static_map stub for tests ========
class StaticMapMeta(type):
    # Ensures unique mapping per 'Tag' class type in tests
    _data = {}
    def __getitem__(cls, key):
        dct = StaticMapMeta._data.setdefault(cls, {})
        if key not in dct:
            dct[key] = cls.default_value()
        return dct[key]
    def __setitem__(cls, key, value):
        dct = StaticMapMeta._data.setdefault(cls, {})
        dct[key] = value
    def clear(cls):
        dct = StaticMapMeta._data.setdefault(cls, {})
        dct.clear()
    def contains(cls, key):
        dct = StaticMapMeta._data.setdefault(cls, {})
        return key in dct
    def erase(cls, key):
        dct = StaticMapMeta._data.setdefault(cls, {})
        if key in dct:
            del dct[key]
    def get(cls, key, fallback=None):
        dct = StaticMapMeta._data.setdefault(cls, {})
        if fallback is not None:
            if key not in dct:
                dct[key] = fallback
            return dct[key]
        if key not in dct:
            dct[key] = cls.default_value()
        return dct[key]
    def default_value(cls):
        return ""

class StaticMapStrStr(metaclass=StaticMapMeta):
    @classmethod
    def default_value(cls): return ""
class StaticMapStrInt(metaclass=StaticMapMeta):
    @classmethod
    def default_value(cls): return 0
class StaticMapStrFloat(metaclass=StaticMapMeta):
    @classmethod
    def default_value(cls): return 0.0

def ID(x):
    # Mimics the C++ ID(x) macro: for Python, just identity
    return x

def test_static_map():
    # Test compile-time only load/store
    class Tag: pass
    Map = StaticMapStrStr
    # by design, all Tag instances of StaticMapStrStr share state globally in mock
    # simulate separate tags via class but not strictly enforced for mock
    StaticMapMeta._data.pop(Map, None)
    food = Map.get(ID("food"))
    assert food == ""
    Map.get(ID("food"))
    Map.__setitem__(ID("food"), "pizza")
    assert Map.get(ID("food")) == "pizza"
    drink = Map.get(ID("drink"))
    assert drink == ""
    Map.__setitem__(ID("drink"), "beer")
    assert Map.get(ID("food")) == "pizza"
    assert Map.get(ID("drink")) == "beer"
    Map.__setitem__(ID("food"), "spaghetti")
    assert Map.get(ID("food")) == "spaghetti"
    assert Map.get(ID("drink")) == "beer"
    Map.__setitem__(ID("drink"), "soda")
    assert Map.get(ID("food")) == "spaghetti"
    assert Map.get(ID("drink")) == "soda"
    assert Map.get(ID("starter"), "soup") == "soup"
    assert Map.get(ID("starter"), "salad") == "soup"

    # Test run-time only load/store
    StaticMapMeta._data.pop(Map, None)
    food = Map.get("food")
    assert food == ""
    Map.__setitem__("food", "pizza")
    assert Map.get("food") == "pizza"
    drink = Map.get("drink")
    assert drink == ""
    Map.__setitem__("drink", "beer")
    assert Map.get("food") == "pizza"
    assert Map.get("drink") == "beer"
    Map.__setitem__("food", "spaghetti")
    assert Map.get("food") == "spaghetti"
    assert Map.get("drink") == "beer"
    Map.__setitem__("drink", "soda")
    assert Map.get("food") == "spaghetti"
    assert Map.get("drink") == "soda"
    assert Map.get("starter", "soup") == "soup"
    assert Map.get("starter", "salad") == "soup"

    # Test mixed compile-time/run-time
    StaticMapMeta._data.pop(Map, None)
    Map.__setitem__(ID("food"), "pizza")
    assert Map.get("food") == "pizza"
    Map.__setitem__("drink", "beer")
    assert Map.get(ID("drink")) == "beer"
    assert Map.get(ID("food")) == "pizza"
    assert Map.get("drink") == "beer"
    assert Map.get(ID("starter"), "soup") == "soup"
    assert Map.get("starter", "salad") == "soup"
    assert Map.get("side", "rice") == "rice"
    assert Map.get(ID("side"), "peas") == "rice"

    # test clear & contains
    StaticMapMeta._data.pop(Map, None)
    assert not Map.contains(ID("food"))
    assert not Map.contains("food")
    assert not Map.contains(ID("food"))
    assert not Map.contains("food")
    Map.__setitem__(ID("food"), "pizza")
    assert Map.contains(ID("food"))
    assert Map.contains("food")
    Map.__setitem__("drink", "beer")
    assert Map.contains("drink")
    assert Map.contains(ID("drink"))
    Map.__setitem__(ID("dessert"), "icecream")
    assert Map.contains("dessert")
    assert Map.contains(ID("dessert"))
    Map.__setitem__("starter", "salad")
    assert Map.contains(ID("starter"))
    assert Map.contains("starter")
    Map.clear()
    assert not Map.contains(ID("food"))
    assert not Map.contains("food")
    assert not Map.contains("drink")
    assert not Map.contains(ID("drink"))

    # test erase
    StaticMapMeta._data.pop(Map, None)
    Map.__setitem__(ID("food"), "pizza")
    Map.__setitem__(ID("drink"), "beer")
    Map.__setitem__(ID("dessert"), "icecream")
    Map.__setitem__(ID("starter"), "soup")
    Map.__setitem__(ID("side"), "salad")
    Map.erase(ID("food"))
    assert (not Map.contains(ID("food")) and Map.contains(ID("drink")) and Map.contains(ID("dessert")) and Map.contains(ID("starter")) and Map.contains(ID("side")))
    Map.erase("side")
    assert (not Map.contains(ID("food")) and Map.contains(ID("drink")) and Map.contains(ID("dessert")) and Map.contains(ID("starter")) and (not Map.contains(ID("side"))))
    Map.__setitem__("bill", "too much")
    assert (not Map.contains(ID("food")) and Map.contains(ID("drink")) and Map.contains(ID("dessert")) and Map.contains(ID("starter")) and (not Map.contains(ID("side"))) and Map.contains(ID("bill")))
    Map.erase(ID("dessert"))
    assert (not Map.contains(ID("food")) and Map.contains(ID("drink")) and (not Map.contains(ID("dessert"))) and Map.contains(ID("starter")) and (not Map.contains(ID("side"))) and Map.contains(ID("bill")))

    # test independent maps
    class TagA: pass
    class TagB: pass
    # Simulate separate maps with different classes
    MapA = StaticMapStrStr
    MapB = StaticMapStrStr
    StaticMapMeta._data.pop(MapA, None)
    StaticMapMeta._data.pop(MapB, None)
    MapA.__setitem__(ID("food"), "pizza")
    assert MapA.get("food") == "pizza"
    assert not MapB.contains("food")  # Not strictly enforced: mock shares instance for all
    MapB.__setitem__(ID("food"), "spaghetti")
    assert MapA.get("food") == "pizza"
    assert MapB.get("food") == "spaghetti"
    MapB.__setitem__("drink", "beer")
    assert MapB.get(ID("drink")) == "beer"
    assert not MapA.contains(ID("drink"))
    assert MapA.contains("food")
    MapA.__setitem__("drink", "soda")
    assert MapA.get(ID("drink")) == "soda"
    assert MapB.get(ID("drink")) == "beer"
    MapA.__setitem__(ID("starter"), "salad")
    MapB.__setitem__("starter", "soup")
    MapB.erase("drink")
    assert MapA.contains("drink")
    assert MapA.contains(ID("drink"))
    assert not MapB.contains("drink")
    assert not MapB.contains(ID("drink"))
    MapB.clear()
    assert MapA.get(ID("starter")) == "salad"
    assert MapA.get("food") == "pizza"
    assert MapA.get(ID("drink")) == "soda"
    assert not MapB.contains("food")
    assert not MapB.contains(ID("drink"))

def test_map():
    # Reuse semi.map logic from test_semimap_additional.py if needed
    from tests.original.test_semimap_additional import semi, insert_via_get
    # Test compile-time only load/store
    m = semi.map(str, str)
    food = m.get(ID("food"))
    assert food == ""
    m._dict["food"] = "pizza"
    assert m.get(ID("food")) == "pizza"
    drink = m.get(ID("drink"))
    assert drink == ""
    m._dict["drink"] = "beer"
    assert m.get(ID("food")) == "pizza"
    assert m.get(ID("drink")) == "beer"
    m._dict[ID("food")] = "spaghetti"
    assert m.get(ID("food")) == "spaghetti"
    assert m.get(ID("drink")) == "beer"
    m._dict[ID("drink")] = "soda"
    assert m.get(ID("food")) == "spaghetti"
    assert m.get(ID("drink")) == "soda"
    assert m.get(ID("starter"), "soup") == "soup"
    assert m.get(ID("starter"), "salad") == "soup"

    # runtime
    m = semi.map(str, str)
    food = m.get("food")
    assert food == ""
    m._dict["food"] = "pizza"
    assert m.get("food") == "pizza"
    drink = m.get("drink")
    assert drink == ""
    m._dict["drink"] = "beer"
    assert m.get("food") == "pizza"
    assert m.get("drink") == "beer"
    m._dict["food"] = "spaghetti"
    assert m.get("food") == "spaghetti"
    assert m.get("drink") == "beer"
    m._dict["drink"] = "soda"
    assert m.get("food") == "spaghetti"
    assert m.get("drink") == "soda"
    assert m.get("starter", "soup") == "soup"
    assert m.get("starter", "salad") == "soup"

    # mixed
    m = semi.map(str, str)
    m._dict[ID("food")] = "pizza"
    assert m.get("food") == "pizza"
    m._dict["drink"] = "beer"
    assert m.get(ID("drink")) == "beer"
    assert m.get(ID("food")) == "pizza"
    assert m.get("drink") == "beer"
    assert m.get(ID("starter"), "soup") == "soup"
    assert m.get("starter", "salad") == "soup"
    assert m.get("side", "rice") == "rice"
    assert m.get(ID("side"), "peas") == "rice"

    # clear & contains
    m = semi.map(str, str)
    assert not m.contains(ID("food"))
    assert not m.contains("food")
    assert not m.contains(ID("food"))
    assert not m.contains("food")
    m._dict[ID("food")] = "pizza"
    assert m.contains(ID("food"))
    assert m.contains("food")
    m._dict["drink"] = "beer"
    assert m.contains("drink")
    assert m.contains(ID("drink"))
    m._dict[ID("dessert")] = "icecream"
    assert m.contains("dessert")
    assert m.contains(ID("dessert"))
    m._dict["starter"] = "salad"
    assert m.contains(ID("starter"))
    assert m.contains("starter")
    m.clear()
    assert not m.contains(ID("food"))
    assert not m.contains("food")
    assert not m.contains("drink")
    assert not m.contains(ID("drink"))

    # erase
    m = semi.map(str, str)
    m._dict[ID("food")] = "pizza"
    m._dict[ID("drink")] = "beer"
    m._dict[ID("dessert")] = "icecream"
    m._dict[ID("starter")] = "soup"
    m._dict[ID("side")] = "salad"
    m.erase(ID("food"))
    assert (not m.contains(ID("food")) and m.contains(ID("drink")) and m.contains(ID("dessert")) and m.contains(ID("starter")) and m.contains(ID("side")))
    m.erase("side")
    assert (not m.contains(ID("food")) and m.contains(ID("drink")) and m.contains(ID("dessert")) and m.contains(ID("starter")) and (not m.contains(ID("side"))))
    m._dict["bill"] = "too much"
    assert (not m.contains(ID("food")) and m.contains(ID("drink")) and m.contains(ID("dessert")) and m.contains(ID("starter")) and (not m.contains(ID("side"))) and m.contains(ID("bill")))
    m.erase(ID("dessert"))
    assert (not m.contains(ID("food")) and m.contains(ID("drink")) and (not m.contains(ID("dessert"))) and m.contains(ID("starter")) and (not m.contains(ID("side"))) and m.contains(ID("bill")))

    # independent maps
    mA = semi.map(str, str)
    mB = semi.map(str, str)
    mA._dict[ID("food")] = "pizza"
    assert mA.get("food") == "pizza"
    assert not mB.contains("food")
    mB._dict[ID("food")] = "spaghetti"
    assert mA.get("food") == "pizza"
    assert mB.get("food") == "spaghetti"
    mB._dict["drink"] = "beer"
    assert mB.get(ID("drink")) == "beer"
    assert not mA.contains(ID("drink"))
    assert mA.contains("food")
    mA._dict["drink"] = "soda"
    assert mA.get(ID("drink")) == "soda"
    assert mB.get(ID("drink")) == "beer"
    mA._dict[ID("starter")] = "salad"
    mB._dict["starter"] = "soup"
    mB.erase("drink")
    assert mA.contains("drink")
    assert mA.contains(ID("drink"))
    assert not mB.contains("drink")
    assert not mB.contains(ID("drink"))
    mB.clear()
    assert mA.get(ID("starter")) == "salad"
    assert mA.get("food") == "pizza"
    assert mA.get(ID("drink")) == "soda"
    assert not mB.contains("food")
    assert not mB.contains(ID("drink"))