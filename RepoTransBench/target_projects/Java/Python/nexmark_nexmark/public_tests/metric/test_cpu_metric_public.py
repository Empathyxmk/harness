import pytest

class CpuMetric:
    def __init__(self, processCpuTimeSeconds, processTotalCpuMilliseconds, processCpuLoad, systemCpuLoad, hostName):
        self._processCpuTimeSeconds = processCpuTimeSeconds
        self._processTotalCpuMilliseconds = processTotalCpuMilliseconds
        self._processCpuLoad = processCpuLoad
        self._systemCpuLoad = systemCpuLoad
        self._hostName = hostName

    def getProcessCpuTimeSeconds(self):
        return self._processCpuTimeSeconds
    def getProcessTotalCpuMilliseconds(self):
        return self._processTotalCpuMilliseconds
    def getProcessCpuLoad(self):
        return self._processCpuLoad
    def getSystemCpuLoad(self):
        return self._systemCpuLoad
    def getHostName(self):
        return self._hostName
    def __str__(self):
        return f"CpuMetric[{self._hostName}]"

def test_cpu_metric_different_values():
    metric = CpuMetric(234.56, 1900, 14.7, 100.2, "nodeX")
    assert metric.getProcessCpuTimeSeconds() == 234.56
    assert metric.getProcessTotalCpuMilliseconds() == 1900
    assert metric.getProcessCpuLoad() == 14.7
    assert metric.getSystemCpuLoad() == 100.2
    assert metric.getHostName() == "nodeX"

def test_to_string_not_empty():
    metric = CpuMetric(0.99, 99, 2.2, 88.1, "hostY")
    s = str(metric)
    assert "hostY" in s
    assert len(s) > 0