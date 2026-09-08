import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from src.volume_meter import VolumeMeter, QColor, Qt

def test_volume_meter_channels():
    vm = VolumeMeter(channel_count=3)
    assert vm.channel_count == 3
    for i in range(3):
        assert vm.get_value(i) == 0.0

def test_volume_meter_set_values():
    vm = VolumeMeter(channel_count=2)
    vm.set_value(0, 0.7)
    vm.set_value(1, 0.15)
    assert vm.get_value(0) == 0.7
    assert vm.get_value(1) == 0.15

def test_volume_meter_qcolor_conversion():
    color = QColor(255, 128, 0)
    assert color.red() == 255
    assert color.green() == 128
    assert color.blue() == 0

def test_volume_meter_qt_enum():
    assert Qt.Horizontal == 1
    assert Qt.Vertical == 2

def test_volume_meter_edge_case_negative_channel():
    vm = VolumeMeter(channel_count=2)
    try:
        vm.get_value(-1)
    except IndexError:
        pass
    else:
        assert False, "Expected IndexError"

def test_volume_meter_edge_case_high_channel():
    vm = VolumeMeter(channel_count=2)
    try:
        vm.get_value(100)
    except IndexError:
        pass
    else:
        assert False, "Expected IndexError"