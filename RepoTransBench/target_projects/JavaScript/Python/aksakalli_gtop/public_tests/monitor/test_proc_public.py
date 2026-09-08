from unittest.mock import MagicMock

class Proc:
    def __init__(self, table):
        self.table = table

    def updateData(self, process_list):
        self.table.setData(process_list)
        self.table.screen.render()

def test_proc_update_table_public():
    table = MagicMock()
    table.setData = MagicMock()
    table.screen = MagicMock()
    table.screen.render = MagicMock()
    proc = Proc(table)

    proc.updateData([
        {
            'pid': 4322,
            'user': 'bob',
            'pr': '19',
            'ni': '0',
            'virt': 102400,
            'res': 50200,
            'shr': 23000,
            's': 'S',
            'cpu': 3.4,
            'mem': 1.6,
            'time': '00:06:45',
            'command': 'postgres'
        },
        {
            'pid': 101,
            'user': 'eve',
            'pr': '20',
            'ni': '0',
            'virt': 15360,
            'res': 8000,
            'shr': 1000,
            's': 'S',
            'cpu': 0.1,
            'mem': 0.3,
            'time': '00:00:18',
            'command': 'cron'
        }
    ])
    assert table.setData.called
    assert table.screen.render.called

def test_proc_update_empty_list_public():
    table = MagicMock()
    table.setData = MagicMock()
    table.screen = MagicMock()
    table.screen.render = MagicMock()
    proc = Proc(table)
    proc.updateData([])
    assert table.setData.called
    assert table.screen.render.called