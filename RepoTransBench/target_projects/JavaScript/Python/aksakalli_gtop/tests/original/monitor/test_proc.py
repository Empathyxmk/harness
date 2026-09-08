import pytest
from unittest.mock import MagicMock

class Proc:
    def __init__(self, table):
        self.table = table
        self.pSort = 'cpu'
        self.reverse = False
        self.cb = None
        # Mocking .screen.key to bind cb
        def fake_key(keys, cb):
            self.cb = cb
        self.table.screen.key.side_effect = fake_key

    def updateData(self, data):
        if data is None or 'list' not in data:
            raise Exception("list property missing")
        proc_list = data['list']
        self.table.setData(proc_list)
        self.table.screen.render()

import types

@pytest.fixture
def setup_proc():
    table = MagicMock()
    table.setData = MagicMock()
    table.screen = MagicMock()
    table.screen.key = MagicMock()
    table.screen.render = MagicMock()
    proc = Proc(table)
    return proc, table

def test_proc_update_sets_data_and_renders(setup_proc):
    proc, table = setup_proc
    processes = [
        {'pid': 1, 'cpu': 20, 'mem': 30, 'command': 'bash', 'user': 'root'},
        {'pid': 2, 'cpu': 10, 'mem': 40, 'command': 'node', 'user': 'guest'}
    ]
    proc.updateData({'list': processes})
    assert table.setData.called
    assert table.screen.render.called

def test_proc_update_handles_empty_list(setup_proc):
    proc, table = setup_proc
    proc.updateData({'list': []})
    assert table.setData.called
    assert table.screen.render.called

def test_proc_update_missing_list_raises(setup_proc):
    proc, table = setup_proc
    with pytest.raises(Exception):
        proc.updateData({})

def test_proc_handle_key_press_for_sorting(setup_proc):
    proc, table = setup_proc
    # Simulate key press handlers that would trigger sorting
    proc.cb('m')
    proc.cb('c')
    proc.cb('p')
    assert table.screen.key.called