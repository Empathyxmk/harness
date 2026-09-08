import pytest

class CpuMetricSender:
    def __init__(self, host, port):
        self._host = host
        self._port = port
    def getHost(self):
        return self._host
    def getPort(self):
        return self._port

def test_metric_sender_host_and_port():
    sender = CpuMetricSender("testhost", 10000)
    assert sender.getHost() == "testhost"
    assert sender.getPort() == 10000

def test_metric_sender_negative_port():
    sender = CpuMetricSender("anotherhost", -1)
    assert sender.getPort() == -1