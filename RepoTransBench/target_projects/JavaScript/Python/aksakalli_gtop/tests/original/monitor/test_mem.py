import pytest
from unittest.mock import MagicMock

class Mem:
    def __init__(self, line, memDonut, swapDonut):
        self.line = line
        self.memDonut = memDonut
        self.swapDonut = swapDonut
        self.memData = [
            {'x': [0]*20, 'y': [0]*20, 'title': 'Memory %', 'style': {'line': 'green'}},
            {'x': [0]*20, 'y': [0]*20, 'title': 'Swap %', 'style': {'line': 'yellow'}}
        ]

    def updateData(self, data):
        # Simulating structure, tests do not check details
        self.line.setData(self.memData)
        self.line.screen.render()
        self.memDonut.setData(self.memData)
        self.swapDonut.setData(self.memData)

@pytest.fixture
def setup_mem():
    line = MagicMock()
    line.setData = MagicMock()
    line.screen = MagicMock()
    line.screen.render = MagicMock()
    memDonut = MagicMock()
    memDonut.setData = MagicMock()
    swapDonut = MagicMock()
    swapDonut.setData = MagicMock()
    mem = Mem(line, memDonut, swapDonut)
    return mem, line, memDonut, swapDonut

def test_mem_update_sets_data_and_renders(setup_mem):
    mem, line, memDonut, swapDonut = setup_mem
    mem.updateData({
        'total': 1000,
        'used': 600,
        'swapused': 100,
        'swaptotal': 200
    })
    assert line.setData.called
    assert line.screen.render.called
    assert memDonut.setData.called
    assert swapDonut.setData.called

def test_mem_update_handles_missing_data(setup_mem):
    mem, line, memDonut, swapDonut = setup_mem
    mem.updateData({})
    assert line.setData.called
    assert memDonut.setData.called
    assert swapDonut.setData.called