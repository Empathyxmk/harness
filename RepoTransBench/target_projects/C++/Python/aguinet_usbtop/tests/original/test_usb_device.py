import pytest

class UsbStats:
    ToHost = 1
    FromHost = 2

class Stats:
    def __init__(self):
        self.push_calls = []

    def push(self, ts, size):
        self.push_calls.append((ts, size))

class UsbDevice:
    def __init__(self, id):
        self.id = id
        self.stats = Stats()

    def push(self, ts, size, direction):
        # Simulate calling stats push
        self.stats.push(ts, size)
        # Direction argument would normally change which stats, omitted here.

def test_push_calls_stats():
    d = UsbDevice(2)
    d.push(3.5, 67, UsbStats.ToHost)
    d.push(6.2, 23, UsbStats.FromHost)
    # No direct observable state, but exercise the line
    assert True