import pytest
from src.lrucache import LRUCache

def test_adds_single_value():
    cache = LRUCache({'maxElements': 1})
    cache.set("foo", 42)
    value = cache.get("foo")
    assert value == 42
    stats = cache.stats()
    assert stats['evictions'] == 0

def test_adds_two_values_and_evicts_oldest():
    cache = LRUCache({'maxElements': 1})
    cache.set("foo", 42)
    cache.set("bar", 21)
    value = cache.get("foo")
    assert value is None
    stats = cache.stats()
    assert stats['evictions'] == 1