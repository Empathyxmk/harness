import pytest
from unittest.mock import MagicMock

class Disk:
    def __init__(self, donut):
        self.donut = donut

    def updateData(self, data):
        self.donut.setData(data)
        self.donut.screen.render()

def test_disk_update_sets_data_and_renders():
    donut = MagicMock()
    donut.setData = MagicMock()
    donut.screen = MagicMock()
    donut.screen.render = MagicMock()
    disk = Disk(donut)

    disk.updateData([{
        'fs': '/dev/sda1',
        'size': 1000,
        'used': 700,
        'use': 70,
        'mount': '/'
    }])
    # The donut.setData was called with a list
    assert isinstance(donut.setData.call_args[0][0], list)
    assert donut.setData.called
    assert donut.screen.render.called

def test_disk_update_handles_no_data():
    donut = MagicMock()
    donut.setData = MagicMock()
    donut.screen = MagicMock()
    donut.screen.render = MagicMock()
    disk = Disk(donut)
    disk.updateData([{
        'fs': None,
        'size': None,
        'used': None,
        'use': None,
        'mount': None
    }])
    assert donut.setData.called
    assert donut.screen.render.called