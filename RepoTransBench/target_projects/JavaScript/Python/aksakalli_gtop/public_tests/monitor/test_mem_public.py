import pytest
from unittest.mock import MagicMock

class Mem:
    def __init__(self, donut):
        self.donut = donut

    def updateData(self, data):
        if data is None:
            return
        self.donut.setData([data])
        self.donut.screen.render()

def test_mem_construct_and_update_public():
    donut = MagicMock()
    donut.setData = MagicMock()
    donut.screen = MagicMock()
    donut.screen.render = MagicMock()
    mem = Mem(donut)

    mem.updateData({
        'total': 16384,
        'used': 4096,
        'free': 12288,
        'swapTotal': 2048,
        'swapUsed': 1024,
        'swapFree': 1024
    })
    # The setData is called with a list
    assert isinstance(donut.setData.call_args[0][0], list)
    assert donut.setData.called
    assert donut.screen.render.called

def test_mem_handle_null_data_public():
    donut = MagicMock()
    donut.setData = MagicMock()
    donut.screen = MagicMock()
    donut.screen.render = MagicMock()
    mem = Mem(donut)
    mem.updateData(None)
    assert not donut.setData.called
    assert not donut.screen.render.called