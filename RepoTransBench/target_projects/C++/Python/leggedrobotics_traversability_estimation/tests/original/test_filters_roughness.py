import pytest
import numpy as np
from src.traversability.roughness_filter import DummyRoughnessFilter

class DummyGridMap:
    def __init__(self, layers):
        # layers: list of str
        self.layers = {name: np.zeros((1, 1)) for name in layers}
    def setGeometry(self, size, res):
        self.shape = (int(size[0]), int(size[1]))
    def getGridIndexes(self):
        # Mimic grid index iteration for 1x1 grid
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
    filter = DummyRoughnessFilter()
    filter.setParam("critical_value", 0.4)
    filter.setParam("estimation_radius", 0.5)
    filter.setParam("map_type", "rough")
    assert filter.configure()
    assert filter.criticalValue_ == pytest.approx(0.4)
    assert filter.estimationRadius_ == pytest.approx(0.5)
    assert filter.type_ == "rough"

def test_configure_failures():
    filter = DummyRoughnessFilter()
    filter.setParam("estimation_radius", 0.3)
    filter.setParam("map_type", "type")
    assert not filter.configure()
    filter.setParam("critical_value", -0.1)
    assert not filter.configure()
    filter.setParam("critical_value", 0.3)
    filter.setParam("estimation_radius", -0.1)
    assert not filter.configure()
    filter.setParam("estimation_radius", 0.3)
    filter.params_.pop("map_type", None)
    assert not filter.configure()

def test_update():
    filter = DummyRoughnessFilter()
    filter.criticalValue_ = 0.4
    filter.estimationRadius_ = 0.5
    filter.type_ = "rough"
    map = DummyGridMap(["elevation", "surface_normal_x", "surface_normal_y", "surface_normal_z"])
    map.setGeometry((1,1), 1.0)
    # Assign test values
    for idx in map.getGridIndexes():
        map["elevation"][idx] = 0.1
        map["surface_normal_x"][idx] = 0
        map["surface_normal_y"][idx] = 0
        map["surface_normal_z"][idx] = 1
    outMap = DummyGridMap([])
    assert filter.update(map, outMap)
    assert outMap.exists("rough")
    badMap = DummyGridMap(["elevation"])
    badMap.setGeometry((1,1), 1.0)
    badOut = DummyGridMap([])
    assert filter.update(badMap, badOut)