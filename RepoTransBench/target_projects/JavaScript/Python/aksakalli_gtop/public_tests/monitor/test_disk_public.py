from unittest.mock import MagicMock

class Disk:
    def __init__(self, donut):
        self.donut = donut

    def updateData(self, data):
        self.donut.setData(data)
        self.donut.screen.render()

def test_disk_update_interval_public():
    donut = MagicMock()
    donut.setData = MagicMock()
    donut.screen = MagicMock()
    donut.screen.render = MagicMock()
    disk = Disk(donut)

    disk.updateData([{
        'fs': '/dev/sdb2',
        'size': 5000,
        'used': 1234,
        'use': 25,
        'mount': '/mnt'
    }])
    assert isinstance(donut.setData.call_args[0][0], list)
    assert donut.setData.called
    assert donut.screen.render.called

def test_disk_null_fields_public():
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