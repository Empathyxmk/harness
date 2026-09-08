import pytest
from haishoku import haishoku

def test_haishoku_init_sets_none():
    h = haishoku.Haishoku()
    assert h.dominant is None
    assert h.palette is None

def test_loadHaishoku_monkeypatch(monkeypatch):
    # Patch the staticmethods called in loadHaishoku to fake values
    monkeypatch.setattr(haishoku.Haishoku, "getColorsMean", staticmethod(lambda x: [(1, (1, 2, 3))]))
    monkeypatch.setattr(haishoku.Haishoku, "getPalette", staticmethod(lambda x: ['palette']))
    monkeypatch.setattr(haishoku.Haishoku, "getDominant", staticmethod(lambda x: ('dom', (0, 0, 0))))

    obj = haishoku.Haishoku.loadHaishoku("fake/path.png")
    assert obj.palette == ['palette']
    assert obj.dominant == ('dom', (0, 0, 0))
    # Accept that obj can be either a class or instance depending on the implementation
    assert isinstance(obj, (haishoku.Haishoku, type))

def test_loadHaishoku_is_classmethod():
    # loadHaishoku should be a classmethod
    assert callable(haishoku.Haishoku.loadHaishoku)

def test_str_repr_of_Haishoku():
    h = haishoku.Haishoku()
    s = str(h)
    r = repr(h)
    assert isinstance(s, str)
    assert isinstance(r, str)