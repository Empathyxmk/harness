import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from src.volume_meter import VolumeMeter, QColor, Qt

def test_public_volume_meter_channels():
    vm = VolumeMeter(channel_count=4)
    assert vm.channel_count == 4
    for i in range(4):
        assert vm.get_value(i) == 0.0

def test_public_volume_meter_set_multiple_values():
    vm = VolumeMeter(channel_count=2)
    vm.set_value(0, 0.4)
    vm.set_value(1, 0.8)
    assert vm.get_value(0) == 0.4
    assert vm.get_value(1) == 0.8

def test_public_qcolor_basic():
    color = QColor(120, 130, 140)
    assert color.red() == 120
    assert color.green() == 130
    assert color.blue() == 140

def test_public_qt_enum():
    assert Qt.Horizontal == 1
    assert Qt.Vertical == 2

def test_public_volume_meter_invalid_set():
    vm = VolumeMeter(channel_count=1)
    try:
        vm.set_value(10, 0.25)
    except IndexError:
        pass
    else:
        assert False, "Expected IndexError"