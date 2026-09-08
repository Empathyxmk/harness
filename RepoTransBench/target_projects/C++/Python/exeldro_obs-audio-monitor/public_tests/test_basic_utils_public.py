import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from src.volume_meter import VolumeMeter

def test_public_volume_meter_init():
    vm = VolumeMeter(channel_count=1)
    assert vm.channel_count == 1
    assert vm.values == [0.0]

def test_public_volume_meter_set_value():
    vm = VolumeMeter(channel_count=1)
    vm.set_value(0, 0.55)
    assert vm.get_value(0) == 0.55

def test_public_volume_meter_invalid_index():
    vm = VolumeMeter(channel_count=1)
    try:
        vm.get_value(99)
    except IndexError:
        pass
    else:
        assert False, "Expected IndexError"