import pytest
import numpy as np
from src.traversability.roughness_filter import DummyRoughnessFilter

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
    filter = DummyRoughnessFilter()
    filter.setParam("critical_value", 0.6)
    filter.setParam("estimation_radius", 0.7)
    filter.setParam("map_type", "roughness_new")
    assert filter.configure()
    assert filter.criticalValue_ == pytest.approx(0.6)
    assert filter.estimationRadius_ == pytest.approx(0.7)
    assert filter.type_ == "roughness_new"

def test_configure_failures():
    filter = DummyRoughnessFilter()
    filter.setParam("critical_value", 0.5)
    filter.setParam("map_type", "typeX")
    assert not filter.configure()
    filter.setParam("estimation_radius", -0.2)
    assert not filter.configure()
    filter.setParam("critical_value", -0.35)
    filter.setParam("estimation_radius", 0.5)
    assert not filter.configure()
    filter.params_.pop("map_type", None)
    filter.setParam("critical_value", 0.8)
    filter.setParam("estimation_radius", 0.2)
    assert not filter.configure()

def test_update():
    filter = DummyRoughnessFilter()
    filter.criticalValue_ = 0.9
    filter.estimationRadius_ = 0.15
    filter.type_ = "roughnessLayerPublic"
    map = DummyGridMap(["elevation", "surface_normal_x", "surface_normal_y", "surface_normal_z"])
    map.setGeometry((2,2), 2.0)
    for idx in map.getGridIndexes():
        map["elevation"][idx] = 0.2
        map["surface_normal_x"][idx] = 0.1
        map["surface_normal_y"][idx] = 0.2
        map["surface_normal_z"][idx] = 0.99
    outMap = DummyGridMap([])
    assert filter.update(map, outMap)
    assert outMap.exists("roughnessLayerPublic")
    badMap = DummyGridMap(["elevation"])
    badMap.setGeometry((1,1), 0.5)
    badOut = DummyGridMap([])
    assert filter.update(badMap, badOut)