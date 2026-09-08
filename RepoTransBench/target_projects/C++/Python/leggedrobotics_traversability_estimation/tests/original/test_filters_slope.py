import pytest
import numpy as np
from src.traversability.slope_filter import DummySlopeFilter

class DummyGridMap:
    def __init__(self, layers):
        self.layers = {name: np.zeros((1, 1)) for name in layers}
    def setGeometry(self, size, res):
        self.shape = (int(size[0]), int(size[1]))
    def getGridIndexes(self):
        return [(0, 0)]
    def __getitem__(self, item):
        return self.layers[item]
    def at(self, layer, idx):
        return self.layers[layer][idx]
    def exists(self, layer):
        return layer in self.layers
    def get_shape(self):
        return (1, 1)

def test_configure_nominal():
    filter = DummySlopeFilter()
    filter.setParam("critical_value", np.pi/4)
    filter.setParam("map_type", "type")
    assert filter.configure()

def test_configure_failures():
    filter = DummySlopeFilter()
    filter.setParam("critical_value", -0.1)
    filter.setParam("map_type", "foo")
    assert not filter.configure()
    filter.setParam("critical_value", 100.0)
    assert not filter.configure()
    filter.setParam("critical_value", np.pi/4)
    filter.params_.pop("map_type", None)
    assert not filter.configure()

def test_update():
    filter = DummySlopeFilter()
    filter.criticalValue_ = np.pi/4
    filter.type_ = "slope"
    map = DummyGridMap(["surface_normal_z"])
    map.setGeometry((1,1), 1.0)
    for idx in map.getGridIndexes():
        map["surface_normal_z"][idx] = 1.0
    outMap = DummyGridMap([])
    assert filter.update(map, outMap)
    assert outMap.exists("slope")
    badMap = DummyGridMap(["foo"])
    badMap.setGeometry((1,1), 1.0)
    badOut = DummyGridMap([])
    assert filter.update(badMap, badOut)