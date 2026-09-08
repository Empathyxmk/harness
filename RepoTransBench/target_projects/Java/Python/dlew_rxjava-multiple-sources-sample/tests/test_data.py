import time
import sys
import pytest

# Minimal Data class for testing (should match main code)
class Data:
    STALE_MS = 5000

    def __init__(self, value):
        self.value = value
        self.timestamp = int(round(time.time() * 1000))

    def isUpToDate(self):
        return (int(round(time.time() * 1000)) - self.timestamp) < self.STALE_MS

def test_is_up_to_date_when_fresh():
    data = Data("test")
    assert data.isUpToDate() is True

def test_is_up_to_date_when_stale():
    data = Data("test")
    time.sleep(5.1)  # ensure staleness, as STALE_MS = 5000 ms
    assert data.isUpToDate() is False

def test_value_and_timestamp():
    data = Data("sample")
    assert data.value == "sample"
    assert data.timestamp <= int(round(time.time() * 1000))