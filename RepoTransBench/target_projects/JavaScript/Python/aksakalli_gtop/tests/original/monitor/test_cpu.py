import pytest
from unittest.mock import MagicMock, patch

class FakeSI:
    def __init__(self):
        self.currentLoad = MagicMock()

class Cpu:
    def __init__(self, line):
        self.line = line
        self.cpuData = []
        self._init_called = False
        self.interval_callbacks = []
        self._set_mock_currentLoad()

    def _set_mock_currentLoad(self):
        def currentLoad(cb):
            self.interval_callbacks.append(cb)
        self.si = FakeSI()
        self.si.currentLoad = currentLoad

    def updateData(self, data):
        # Simulating logic, focusing on test coverage
        # Assume data is like {'cpus': [{'load': 10.123}, ...]}
        if 'cpus' in data:
            self.cpuData = []
            for idx, cpu in enumerate(data['cpus']):
                self.cpuData.append({'title': f'CPU{idx+1}: {cpu["load"]}%', 'y': [cpu['load']]})
            self.line.setData(self.cpuData)
            self.line.screen.render()

@pytest.fixture
def setup_cpu():
    line = MagicMock()
    line.setData = MagicMock()
    line.screen = MagicMock()
    line.screen.render = MagicMock()
    cpu = Cpu(line)
    return cpu, line

def test_cpu_init_and_update(setup_cpu):
    cpu, line = setup_cpu
    # Simulate the initial callback for system info
    fakeData = {'cpus': [{'load': 10.123}, {'load': 50.1}]}
    cpu.updateData(fakeData)
    assert len(cpu.cpuData) == 2
    assert 'CPU1' in cpu.cpuData[0]['title']
    assert isinstance(cpu.cpuData[0]['y'], list)
    newData = {'cpus': [{'load': 77.77}, {'load': 22.4}]}
    cpu.updateData(newData)
    assert line.setData.called
    assert line.screen.render.called
    assert '%' in cpu.cpuData[0]['title']
    assert '%' in cpu.cpuData[1]['title']