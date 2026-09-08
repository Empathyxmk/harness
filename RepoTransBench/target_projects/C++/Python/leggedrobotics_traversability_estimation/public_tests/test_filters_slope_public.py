import pytest
import numpy as np
from src.traversability.slope_filter import DummySlopeFilter

class DummyGridMap:
    def __init__(self, layers):
        self.layers = {name: np.zeros((2, 2)) for name in layers}
    def setGeometry(self, size, res):
        self.shape = (int(size[0]), int(size[1]))
    def getGridIndexes(self):
        return [(x, y) for x in range(2) for y in range(2)]
    def __getitem__(self, item):
        return self.layers[item]
    def at(self, layer, idx):
        return self.layers[layer][idx]
    def exists(self, layer):
        return layer in self.layers
    def get_shape(self):
        return (2, 2)

def test_configure_nominal():
    filter = DummySlopeFilter()
    filter.setParam("critical_value", np.pi / 2.0 / 3.0)
    filter.setParam("map_type", "slope_special")
    assert filter.configure()

def test_configure_failures():
    filter = DummySlopeFilter()
    filter.setParam("critical_value", -3.5)
    filter.setParam("map_type", "typeY")
    assert not filter.configure()
    filter.setParam("critical_value", 120.0)
    assert not filter.configure()
    filter.setParam("critical_value", np.pi/3)
    filter.params_.pop("map_type", None)
    assert not filter.configure()

def test_update():
    filter = DummySlopeFilter()
    filter.criticalValue_ = np.pi / 5.0
    filter.type_ = "slopePublic"
    map = DummyGridMap(["surface_normal_z"])
    map.setGeometry((2,2), 0.7)
    for idx in map.getGridIndexes():
        map["surface_normal_z"][idx] = 0.93
    outMap = DummyGridMap([])
    assert filter.update(map, outMap)
    assert outMap.exists("slopePublic")
    badMap = DummyGridMap(["example"])
    badMap.setGeometry((1,1), 1.5)
    badOut = DummyGridMap([])
    assert filter.update(badMap, badOut)