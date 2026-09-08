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
    def getCopy(self, key):
        return self.get(key)
    def _enforce_limits(self):
        while len(self.data) > self.max_allowed:
            oldest = self.lru.pop(0)
            del self.data[oldest]

Cache = SimpleLRUCache
lru11 = type('lru11', (), {"Cache": Cache, "KeyNotFound": KeyNotFound})

def test_insert_and_eviction():
    cache = lru11.Cache(3, 1)
    cache.insert("alpha", 100)
    cache.insert("beta", 200)
    cache.insert("gamma", 300)
    cache.insert("delta", 400)  # Should evict "alpha"
    assert cache.size() == 3
    with pytest.raises(KeyNotFound):
        cache.get("alpha")

def test_update_refresh():
    cache = lru11.Cache(2)
    cache.insert("dog", 99)
    cache.insert("cat", 88)
    cache.insert("dog", 77)  # update
    assert cache.get("dog") == 77

def test_clear_and_empty():
    cache = lru11.Cache(4)
    cache.insert("x", 1)
    cache.insert("y", 2)
    cache.clear()
    assert cache.empty()
    assert cache.size() == 0

def test_exception_key_not_found():
    cache = lru11.Cache(1)
    with pytest.raises(KeyNotFound):
        cache.get("notfoundkey")

def test_emplace_and_getCopy():
    cache = lru11.Cache(2)
    cache.emplace(1001, 501)
    assert cache.getCopy(1001) == 501