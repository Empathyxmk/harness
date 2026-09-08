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
    filter.setParam("critical_value", 0.3)
    filter.setParam("first_window_radius", 0.04)
    filter.setParam("second_window_radius", 0.06)
    filter.setParam("critical_cell_number", 4)
    filter.setParam("map_type", "foo")
    assert filter.configure()
    assert filter.criticalValue_ == pytest.approx(0.3)
    assert filter.firstWindowRadius_ == pytest.approx(0.04)
    assert filter.secondWindowRadius_ == pytest.approx(0.06)
    assert filter.nCellCritical_ == 4
    assert filter.type_ == "foo"

def test_configure_failures():
    filter = DummyStepFilter()
    filter.setParam("critical_value", -0.3)
    filter.setParam("first_window_radius", 0.06)
    filter.setParam("second_window_radius", 0.06)
    filter.setParam("critical_cell_number", 4)
    filter.setParam("map_type", "foo")
    assert not filter.configure()
    filter.setParam("critical_value", 0.3)
    filter.setParam("first_window_radius", -0.05)
    assert not filter.configure()
    filter.setParam("first_window_radius", 0.05)
    filter.setParam("second_window_radius", -0.03)
    assert not filter.configure()
    filter.setParam("second_window_radius", 0.03)
    filter.setParam("critical_cell_number", 0)
    assert not filter.configure()
    filter.setParam("critical_cell_number", 4)
    filter.params_.pop("map_type", None)
    assert not filter.configure()

def test_update():
    filter = DummyStepFilter()
    filter.criticalValue_ = 0.3
    filter.firstWindowRadius_ = 0.08
    filter.secondWindowRadius_ = 0.08
    filter.nCellCritical_ = 1
    filter.type_ = "step"
    map = DummyGridMap(["elevation"])
    map.setGeometry((1,1), 1.0)
    for idx in map.getGridIndexes():
        map["elevation"][idx] = 0.1
    outMap = DummyGridMap([])
    assert filter.update(map, outMap)
    assert outMap.exists("step")
    assert outMap.exists("step_height")
    badMap = DummyGridMap(["foo"])
    badMap.setGeometry((1,1), 1.0)
    badOut = DummyGridMap([])
    assert filter.update(badMap, badOut)