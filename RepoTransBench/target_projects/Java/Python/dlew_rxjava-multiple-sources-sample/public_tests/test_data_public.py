import time
import pytest

class Data:
    STALE_MS = 5000

    def __init__(self, value):
        self.value = value
        self.timestamp = int(round(time.time() * 1000))

    def isUpToDate(self):
        return (int(round(time.time() * 1000)) - self.timestamp) < self.STALE_MS

def test_is_up_to_date_when_fresh_public():
    data = Data("public")
    assert data.isUpToDate() is True

def test_is_up_to_date_when_stale_public():
    data = Data("anotherPublic")
    time.sleep(5.2) # over STALE_MS
    assert data.isUpToDate() is False

def test_value_and_timestamp_public():
    data = Data("differentSample")
    assert data.value == "differentSample"
    assert data.timestamp <= int(round(time.time() * 1000))