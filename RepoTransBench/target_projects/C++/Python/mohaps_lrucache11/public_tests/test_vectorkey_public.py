import pytest

class KeyNotFound(Exception):
    pass

class VectorKeyCache:
    def __init__(self):
        self.data = dict()

    def insert(self, key, value):
        self.data[tuple(key)] = list(value)

    def get(self, key):
        k = tuple(key)
        if k not in self.data:
            raise KeyNotFound
        return self.data[k]

def test_vector_key_public():
    cache = VectorKeyCache()
    key2 = [4, 5, 6]
    val2 = [10, 20, 30]
    cache.insert(key2, val2)
    ret2 = cache.get(key2)
    assert ret2 == val2