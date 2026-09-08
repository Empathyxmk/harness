import pytest

class DummyCache:
    def __init__(self, file_name):
        self.file_name = file_name
        self.times_fetched = 0

    def fetch(self):
        self.times_fetched += 1
        return f"fetched_public_{self.file_name}"

    def get_times_fetched(self):
        return self.times_fetched

def test_fetch_returns_file_with_different_name():
    cache = DummyCache("pubfile-2211.txt")
    res = cache.fetch()
    assert "pubfile-2211.txt" in res

def test_fetch_counts_times_fetched_with_different_file():
    cache = DummyCache("pubcache.data")
    cache.fetch()
    cache.fetch()
    assert cache.get_times_fetched() == 2