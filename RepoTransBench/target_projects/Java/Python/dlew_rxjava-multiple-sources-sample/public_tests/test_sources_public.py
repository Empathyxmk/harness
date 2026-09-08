import pytest
import time

class Data:
    STALE_MS = 5000

    def __init__(self, value):
        self.value = value
        self.timestamp = int(round(time.time() * 1000))

    def isUpToDate(self):
        return (int(round(time.time() * 1000)) - self.timestamp) < self.STALE_MS

class Sources:
    def __init__(self):
        self._memory = None
        self._disk = None
        self._request_number = 0

    def clearMemory(self):
        self._memory = None

    def memory(self):
        return [self._memory]

    def disk(self):
        return [self._disk]

    def network(self):
        self._request_number += 1
        value = f"network{self._request_number}"
        data = Data(value)
        self._disk = data
        self._memory = data
        return [data]

class TestSubscriber:
    def __init__(self):
        self.values = []
        self.completed = False

    def subscribe(self, observable):
        self.values.extend(observable)
        self.completed = True

    def assertValue(self, val):
        assert self.values == [val]

    def assertCompleted(self):
        assert self.completed

    def assertValueCount(self, n):
        assert len(self.values) == n

def setup_sources():
    return Sources()

def test_memory_initial_null_public():
    sources = setup_sources()
    test_subscriber = TestSubscriber()
    test_subscriber.subscribe(sources.memory())
    test_subscriber.assertValue(None)
    test_subscriber.assertCompleted()

def test_disk_initial_null_public():
    sources = setup_sources()
    test_subscriber = TestSubscriber()
    test_subscriber.subscribe(sources.disk())
    test_subscriber.assertValue(None)
    test_subscriber.assertCompleted()

def test_network_returns_data_and_caches_to_disk_and_memory_public():
    sources = setup_sources()
    test_subscriber = TestSubscriber()
    test_subscriber.subscribe(sources.network())
    mem = TestSubscriber()
    mem.subscribe(sources.memory())
    mem.assertValueCount(1)
    disk = TestSubscriber()
    disk.subscribe(sources.disk())
    disk.assertValueCount(1)
    test_subscriber.assertCompleted()

def test_clear_memory_public():
    sources = setup_sources()
    sources.network()  # populate memory with some data
    sources.clearMemory()
    test_subscriber = TestSubscriber()
    test_subscriber.subscribe(sources.memory())
    test_subscriber.assertValue(None)