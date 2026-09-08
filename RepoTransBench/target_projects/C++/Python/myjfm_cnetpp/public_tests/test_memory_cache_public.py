import pytest

class MemoryCache:
    def __init__(self):
        self._cache = {}

    def Set(self, key, value):
        self._cache[key] = value

    def Get(self, key, value_out):
        if key in self._cache:
            value_out[0] = self._cache[key]
            return True
        return False

def test_set_and_get():
    cache = MemoryCache()
    cache.Set(111, 222)
    value = [0]
    assert cache.Get(111, value)
    assert value[0] == 222

def test_not_found():
    cache = MemoryCache()
    value = [0]
    assert not cache.Get(54321, value)