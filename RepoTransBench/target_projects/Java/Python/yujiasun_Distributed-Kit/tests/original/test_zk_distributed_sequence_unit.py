from unittest.mock import MagicMock
import pytest

class Stat:
    def __init__(self):
        self._version = 0
    def setVersion(self, v): self._version = v
    def getVersion(self): return self._version

class SetDataBuilder:
    def __init__(self, stat_return=None, exc=None):
        self._stat_return = stat_return
        self._exc = exc
    def withVersion(self, version):
        return self
    def forPath(self, *a, **kw):
        if self._exc:
            raise self._exc
        return self._stat_return

class CuratorFramework:
    def __init__(self, set_data_builder):
        self._sdb = set_data_builder
    def setData(self):
        return self._sdb

class ZkDistributedSequence:
    def __init__(self, client):
        self.max_retries = 3
        self.base_sleep_time_ms = 1000
        self.client = client

    def getMaxRetries(self):
        return self.max_retries
    def setMaxRetries(self, n):
        self.max_retries = n
    def getBaseSleepTimeMs(self):
        return self.base_sleep_time_ms
    def sequence(self, name):
        try:
            # Returns a Stat object with getVersion
            sdb = self.client.setData()
            builder = sdb.withVersion(-1)
            stat = builder.forPath(name, b'somebytes')
            return stat.getVersion()
        except Exception:
            return None

def test_get_set_max_retries():
    seq = ZkDistributedSequence(client=None)
    assert seq.getMaxRetries() == 3
    seq.setMaxRetries(9)
    assert seq.getMaxRetries() == 9

def test_get_base_sleep_time_ms():
    seq = ZkDistributedSequence(client=None)
    assert seq.getBaseSleepTimeMs() == 1000

def test_sequence_returns_value():
    stat = Stat()
    stat.setVersion(17)
    sdb = SetDataBuilder(stat_return=stat)
    client = CuratorFramework(sdb)
    seq = ZkDistributedSequence(client)
    result = seq.sequence("abc")
    assert result == 17

def test_sequence_handles_exception():
    sdb = SetDataBuilder(stat_return=None, exc=RuntimeError("fail!"))
    client = CuratorFramework(sdb)
    seq = ZkDistributedSequence(client)
    result = seq.sequence("failcase")
    assert result is None