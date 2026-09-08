import pytest
from src.lrucache import LRUCache


def test_set_and_retrieve_primitive_values():
    cache = LRUCache()
    cache.set("foo", 42)
    value = cache.get("foo")
    assert value == 42

def test_set_and_retrieve_string_values():
    cache = LRUCache()
    cache.set("foo", "bar")
    value = cache.get("foo")
    assert value == "bar"

def test_set_and_retrieve_object_values():
    cache = LRUCache()
    obj = {"example": 42}
    cache.set("foo", obj)
    value = cache.get("foo")
    assert value is obj

def test_remove_called_removes_specified_item():
    cache = LRUCache()
    cache.set("foo", 42)
    assert cache.get("foo") == 42
    cache.remove("foo")
    value = cache.get("foo")
    assert value is None

def test_size_returns_correct_size():
    cache = LRUCache()
    assert cache.size() == 0
    cache.set("foo", 42)
    assert cache.size() == 1

def test_clear_removes_all_items():
    cache = LRUCache()
    cache.set("foo", 42)
    cache.set("bar", 21)
    cache.clear()
    assert cache.get("foo") is None
    assert cache.get("bar") is None

def test_stats_returns_statistics():
    cache = LRUCache()
    cache.set("foo", 42)
    stats = cache.stats()
    assert stats["size"] == 1
    assert stats["evictions"] == 0