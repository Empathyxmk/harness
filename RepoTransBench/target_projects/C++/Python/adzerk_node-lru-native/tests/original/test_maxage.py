import pytest
import time
from src.lrucache import LRUCache

def test_does_not_expire_value_within_maxage():
    cache = LRUCache({'maxAge': 100})
    cache.set("foo", 42)
    value = cache.get("foo")
    assert value == 42
    stats = cache.stats()
    assert stats['evictions'] == 0

def test_expires_value_after_maxage():
    cache = LRUCache({'maxAge': 100})
    cache.set("foo", 42)
    time.sleep(0.2)
    value = cache.get("foo")
    assert value is None
    stats = cache.stats()
    assert stats['evictions'] == 1