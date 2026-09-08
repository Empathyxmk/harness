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
    def contains(self, key):
        return key in self.data
    def remove(self, key):
        if key in self.data:
            del self.data[key]
            self.lru.remove(key)
    def emplace(self, key, value):
        self.insert(key, value)
    def getCopy(self, key):
        return self.get(key)
    def tryGet(self, key, out):
        if key in self.data:
            return True, self.data[key]
        else:
            return False, out
    def _enforce_limits(self):
        while len(self.data) > self.max_allowed:
            oldest = self.lru.pop(0)
            del self.data[oldest]

Cache = SimpleLRUCache
lru11 = type('lru11', (), {"Cache": Cache, "KeyNotFound": KeyNotFound})

def test_insert_get_clear():
    cache = lru11.Cache(2, 1)
    cache.insert(1, "one")
    cache.insert(2, "two")
    assert cache.size() == 2
    assert not cache.empty()
    assert cache.get(1) == "one"
    assert cache.get(2) == "two"
    cache.clear()
    assert cache.size() == 0
    assert cache.empty()

def test_overflow_prune():
    cache = lru11.Cache(2, 1)
    cache.insert(5, 5)
    cache.insert(6, 6)
    cache.insert(7, 7)
    assert cache.size() <= 2

def test_update_existing_key():
    cache = lru11.Cache(3)
    cache.insert(1, "A")
    cache.insert(1, "B")
    assert cache.get(1) == "B"

def test_emplace():
    cache = lru11.Cache(3)
    cache.emplace(10, "foo")
    assert cache.get(10) == "foo"

def test_getCopy_and_tryGet():
    cache = lru11.Cache(3)
    cache.insert(3, 9)
    v = cache.getCopy(3)
    assert v == 9
    success, v2 = cache.tryGet(3, -1)
    assert success and v2 == 9
    success, _ = cache.tryGet(4, -1)
    assert not success

def test_remove_and_contains():
    cache = lru11.Cache(3)
    cache.insert(1, 2)
    assert cache.contains(1)
    cache.remove(1)
    assert not cache.contains(1)

def test_get_nonexistent_key():
    cache = lru11.Cache(2)
    with pytest.raises(KeyNotFound):
        cache.get(404)

def test_unbounded_cache():
    cache = lru11.Cache(0)
    for i in range(100):
        cache.insert(i, i*i)
    assert cache.size() == 100