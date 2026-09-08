import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from src.volume_meter import VolumeMeter

def test_volume_meter_basic_construction():
    vm = VolumeMeter(channel_count=2)
    assert vm.channel_count == 2
    assert vm.values == [0.0, 0.0]

def test_volume_meter_set_and_get_value():
    vm = VolumeMeter(channel_count=2)
    vm.set_value(0, 0.75)
    assert vm.get_value(0) == 0.75
    vm.set_value(1, 0.5)
    assert vm.get_value(1) == 0.5

def test_volume_meter_overwrite_value():
    vm = VolumeMeter(channel_count=2)
    vm.set_value(0, 0.30)
    vm.set_value(0, 0.60)
    assert vm.get_value(0) == 0.60

def test_volume_meter_invalid_channel():
    vm = VolumeMeter(channel_count=2)
    try:
        vm.set_value(2, 0.2)
    except IndexError:
        pass
    else:
        assert False, "Expected IndexError"