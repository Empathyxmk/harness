import pytest
from src.lrucache import LRUCache

def test_simple_put_different_data():
    cache_lru = LRUCache(1)
    cache_lru.put(42, 4242)
    assert cache_lru.exists(42)
    assert cache_lru.get(42) == 4242
    assert cache_lru.size() == 1

def test_missing_value_different_data():
    cache_lru = LRUCache(1)
    with pytest.raises(KeyError):
        cache_lru.get(1001)

def test_put_existing_key_different_data():
    cache_lru = LRUCache(2)
    cache_lru.put(3, 30)
    cache_lru.put(4, 40)
    assert cache_lru.size() == 2

    # Access 3, it should become most recently used
    assert cache_lru.get(3) == 30

    # Put key 3 again with new value
    cache_lru.put(3, 300)
    assert cache_lru.size() == 2
    assert cache_lru.get(3) == 300

    # Add a new item, key 4 should be evicted
    cache_lru.put(5, 50)
    assert not cache_lru.exists(4)
    assert cache_lru.exists(3)
    assert cache_lru.exists(5)
    assert cache_lru.size() == 2

def test_get_moves_to_front_different_data():
    cache_lru = LRUCache(3)
    cache_lru.put(10, 100)
    cache_lru.put(11, 110)
    cache_lru.put(12, 120)

    # Access 10, moves to front
    assert cache_lru.get(10) == 100

    # Add new item, 11 should be evicted
    cache_lru.put(13, 130)
    assert not cache_lru.exists(11)
    assert cache_lru.exists(10)
    assert cache_lru.exists(12)
    assert cache_lru.exists(13)
    assert cache_lru.size() == 3

def test_capacity_one_lru_different_data():
    cache_lru = LRUCache(1)
    cache_lru.put(101, 12345)
    assert cache_lru.exists(101)
    assert cache_lru.get(101) == 12345

    cache_lru.put(202, 67890) # Should evict 101
    assert not cache_lru.exists(101)
    assert cache_lru.exists(202)
    assert cache_lru.get(202) == 67890

    # Try to get evicted key
    with pytest.raises(KeyError):
        cache_lru.get(101)

def test_insert_many_evict_lru_different_data():
    cache_lru = LRUCache(2)
    cache_lru.put(8, 800)
    cache_lru.put(9, 900)
    cache_lru.put(10, 1000) # evicts 8
    assert not cache_lru.exists(8)
    assert cache_lru.exists(9)
    assert cache_lru.exists(10)
    cache_lru.put(11, 1100) # evicts 9
    assert not cache_lru.exists(9)
    assert cache_lru.exists(10)
    assert cache_lru.exists(11)