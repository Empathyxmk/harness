import pytest
import time

# Minimal Data and Sources for this branch test
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

    def logSource(self, name):
        def decorator(generator):
            output = []
            for data in generator:
                status = None
                if data is None:
                    status = f"{name} does not have any data."
                elif not data.isUpToDate():
                    status = f"{name} has stale data."
                else:
                    status = f"{name} has the data you are looking for!"
                # For real application: print(status)
                output.append(data)
            return output
        return decorator

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

def test_memory_with_fresh_data():
    sources = setup_sources()
    data = Data("fresh")
    sources.network()  # Put it in via network to also store to disk and memory
    test_subscriber = TestSubscriber()
    test_subscriber.subscribe(sources.memory())
    test_subscriber.assertValueCount(1)

def test_disk_with_fresh_data():
    sources = setup_sources()
    sources.network()  # Put data in disk and memory via network
    test_subscriber = TestSubscriber()
    test_subscriber.subscribe(sources.disk())
    test_subscriber.assertValueCount(1)

def test_network_multiple_requests():
    sources = setup_sources()
    data1 = sources.network()[0]
    data2 = sources.network()[0]
    test_subscriber = TestSubscriber()
    test_subscriber.subscribe(sources.memory())
    test_subscriber.assertValueCount(1)
    assert data1.value != data2.value

def test_log_source_null_and_stale():
    sources = setup_sources()
    class StaleData(Data):
        def isUpToDate(self_inner):
            return False
    class FreshData(Data):
        def isUpToDate(self_inner):
            return True

    test_obs = [None, StaleData("x"), FreshData("y")]
    decorated = sources.logSource("UNITTEST")(test_obs)
    test_subscriber = TestSubscriber()
    test_subscriber.subscribe(decorated)
    test_subscriber.assertValueCount(3)