import pytest
import numpy as np
from src.traversability.step_filter import DummyStepFilter

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
    filter = DummyStepFilter()
    filter.setParam("critical_value", 0.11)
    filter.setParam("first_window_radius", 0.12)
    filter.setParam("second_window_radius", 0.13)
    filter.setParam("critical_cell_number", 2)
    filter.setParam("map_type", "step_public")
    assert filter.configure()
    assert filter.criticalValue_ == pytest.approx(0.11)
    assert filter.firstWindowRadius_ == pytest.approx(0.12)
    assert filter.secondWindowRadius_ == pytest.approx(0.13)
    assert filter.nCellCritical_ == 2
    assert filter.type_ == "step_public"

def test_configure_failures():
    filter = DummyStepFilter()
    filter.setParam("critical_value", 0.14)
    filter.setParam("first_window_radius", 0.15)
    filter.setParam("second_window_radius", 0.16)
    filter.setParam("critical_cell_number", 3)
    assert not filter.configure()
    filter.setParam("map_type", "step_public_2")
    filter.setParam("critical_value", -0.2)
    assert not filter.configure()
    filter.setParam("critical_value", 0.18)
    filter.setParam("first_window_radius", -0.19)
    assert not filter.configure()
    filter.setParam("first_window_radius", 0.2)
    filter.setParam("second_window_radius", -0.21)
    assert not filter.configure()
    filter.setParam("second_window_radius", 0.22)
    filter.setParam("critical_cell_number", 0)
    assert not filter.configure()

def test_update():
    filter = DummyStepFilter()
    filter.criticalValue_ = 0.09
    filter.firstWindowRadius_ = 0.33
    filter.secondWindowRadius_ = 0.33
    filter.nCellCritical_ = 1
    filter.type_ = "stepLayerPublic"
    map = DummyGridMap(["elevation"])
    map.setGeometry((1,1), 0.7)
    for idx in map.getGridIndexes():
        map["elevation"][idx] = 0.45
    outMap = DummyGridMap([])
    assert filter.update(map, outMap)
    assert outMap.exists("stepLayerPublic")