import pytest

# For complex keys (like vectors in C++), we will use tuples/lists in Python
class KeyNotFound(Exception):
    pass

class VectorKeyCache:
    def __init__(self):
        self.data = dict()

    def insert(self, key, value):
        # Convert list key to tuple for hashability/safety
        self.data[tuple(key)] = list(value)

    def get(self, key):
        k = tuple(key)
        if k not in self.data:
            raise KeyNotFound
        return self.data[k]

def test_vector_key_cache_basic():
    cache = VectorKeyCache()
    key1 = [1, 2, 3]
    val1 = [0, 0, 1]
    cache.insert(key1, val1)
    ret = cache.get(key1)
    assert ret == val1