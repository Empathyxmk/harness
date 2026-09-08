from unittest.mock import MagicMock

class Cpu:
    def __init__(self, sparkline, line):
        self.sparkline = sparkline
        self.line = line

    def updateData(self, cpu_stats):
        self.sparkline.setData(cpu_stats)
        self.line.setData(cpu_stats)
        self.sparkline.screen.render()
        self.line.screen.render()

def test_cpu_sparkline_line_public():
    sparkline = MagicMock()
    sparkline.setData = MagicMock()
    sparkline.screen = MagicMock()
    sparkline.screen.render = MagicMock()
    line = MagicMock()
    line.setData = MagicMock()
    line.screen = MagicMock()
    line.screen.render = MagicMock()
    cpu = Cpu(sparkline, line)

    cpu.updateData([
        {'times': {'user': 20000, 'nice': 2222, 'sys': 3333, 'idle': 696969, 'irq': 100}},
        {'times': {'user': 15000, 'nice': 1200, 'sys': 1800, 'idle': 50505, 'irq': 80}},
    ])
    assert sparkline.setData.called
    assert line.setData.called
    assert sparkline.screen.render.called
    assert line.screen.render.called

def test_cpu_handle_empty_array_public():
    sparkline = MagicMock()
    sparkline.setData = MagicMock()
    sparkline.screen = MagicMock()
    sparkline.screen.render = MagicMock()
    line = MagicMock()
    line.setData = MagicMock()
    line.screen = MagicMock()
    line.screen.render = MagicMock()
    cpu = Cpu(sparkline, line)
    cpu.updateData([])
    assert sparkline.setData.called
    assert line.setData.called