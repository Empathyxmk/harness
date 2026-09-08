from unittest.mock import MagicMock

class Net:
    def __init__(self, table):
        self.table = table

    def updateData(self, stats):
        self.table.setData(stats)
        self.table.screen.render()

def test_net_update_table_public():
    table = MagicMock()
    table.setData = MagicMock()
    table.screen = MagicMock()
    table.screen.render = MagicMock()
    net = Net(table)
    net.updateData([
        {
            'iface': 'eth2',
            'rx_bytes': 1000888,
            'tx_bytes': 9100,
            'rx_errors': 1,
            'tx_errors': 0
        },
        {
            'iface': 'wlan1',
            'rx_bytes': 8899,
            'tx_bytes': 15663,
            'rx_errors': 0,
            'tx_errors': 0
        }
    ])
    assert table.setData.called
    assert table.screen.render.called

def test_net_handle_empty_public():
    table = MagicMock()
    table.setData = MagicMock()
    table.screen = MagicMock()
    table.screen.render = MagicMock()
    net = Net(table)
    net.updateData([])
    assert table.setData.called
    assert table.screen.render.called