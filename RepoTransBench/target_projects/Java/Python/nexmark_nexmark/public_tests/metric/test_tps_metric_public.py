import pytest

class TpsMetric:
    def __init__(self):
        self._startTime = None
        self._endTime = None
        self._tps = None
        self._num = None

    def setStartTime(self, st):
        self._startTime = st
    def setEndTime(self, et):
        self._endTime = et
    def setTps(self, v):
        self._tps = v
    def setNum(self, n):
        self._num = n

    def getStartTime(self):
        return self._startTime
    def getEndTime(self):
        return self._endTime
    def getTps(self):
        return self._tps
    def getNum(self):
        return self._num

def test_tps_metric_setters_getters():
    metric = TpsMetric()
    metric.setStartTime(22222)
    metric.setEndTime(33333)
    metric.setTps(12345.6)
    metric.setNum(77)
    assert metric.getStartTime() == 22222
    assert metric.getEndTime() == 33333
    assert metric.getTps() == 12345.6
    assert metric.getNum() == 77