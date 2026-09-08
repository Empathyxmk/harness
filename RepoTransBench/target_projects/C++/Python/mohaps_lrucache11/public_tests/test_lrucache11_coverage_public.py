import pytest

class KeyNotFound(Exception):
    pass

class SimpleLRUCache:
    def __init__(self, maxsize, elasticity=0):
        self.maxsize = maxsize
        self.elasticity = elasticity
        self.data = {}
        self.lru = []
        self.max_allowed = maxsize + elasticity if maxsize > 0 else float('inf')

    def insert(self, key, value):
        if key in self.data:
            self.lru.remove(key)
        self.data[key] = value
        self.lru.append(key)
        self._enforce_limits()
    def get(self, key):
        if key not in self.data:
            raise KeyNotFound(key)
        self.lru.remove(key)
        self.lru.append(key)
        return self.data[key]
    def size(self):
        return len(self.data)
    def empty(self):
        return self.size() == 0
    def clear(self):
        self.data.clear()
        self.lru.clear()
    def emplace(self, key, value):
        self.insert(key, value)
    def _enforce_limits(self):
        while len(self.data) > self.max_allowed:
            oldest = self.lru.pop(0)
            del self.data[oldest]
    def getCopy(self, key):
        return self.get(key)

Cache = SimpleLRUCache
lru11 = type('lru11', (), {"Cache": Cache, "KeyNotFound": KeyNotFound})

def test_insert_get_clear_public():
    cache = lru11.Cache(2, 1)
    cache.insert(21, "twenty-one")
    cache.insert(42, "forty-two")
    assert cache.size() == 2
    assert not cache.empty()
    assert cache.get(21) == "twenty-one"
    assert cache.get(42) == "forty-two"
    cache.clear()
    assert cache.size() == 0
    assert cache.empty()

def test_overflow_prune_public():
    cache = lru11.Cache(3, 2)
    cache.insert(12, 120)
    cache.insert(22, 220)
    cache.insert(32, 320)
    cache.insert(42, 420)
    cache.insert(52, 520)
    assert cache.size() <= 3

def test_update_existing_key_public():
    cache = lru11.Cache(2)
    cache.insert(7, "seven")
    cache.insert(7, "updated-seven")
    assert cache.get(7) == "updated-seven"

def test_emplace_public():
    cache = lru11.Cache(2)
    cache.emplace(123, "abc")
    assert cache.get(123) == "abc"