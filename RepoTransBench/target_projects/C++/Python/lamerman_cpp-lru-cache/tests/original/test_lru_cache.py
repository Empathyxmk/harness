import pytest
from src.lrucache import LRUCache

NUM_OF_TEST1_RECORDS = 100
NUM_OF_TEST2_RECORDS = 100
TEST2_CACHE_CAPACITY = 50

def test_simple_put():
    cache_lru = LRUCache(1)
    cache_lru.put(7, 777)
    assert cache_lru.exists(7)
    assert cache_lru.get(7) == 777
    assert cache_lru.size() == 1

def test_missing_value():
    cache_lru = LRUCache(1)
    with pytest.raises(KeyError):
        cache_lru.get(7)

def test_put_existing_key():
    cache_lru = LRUCache(2)
    cache_lru.put(1, 10)
    cache_lru.put(2, 20)
    assert cache_lru.size() == 2

    # Access 1, it should become most recently used
    assert cache_lru.get(1) == 10

    # Put key 1 again with new value
    cache_lru.put(1, 100)
    assert cache_lru.size() == 2
    assert cache_lru.get(1) == 100

    # Add a new item, key 2 should be evicted
    cache_lru.put(3, 30)
    assert not cache_lru.exists(2)
    assert cache_lru.exists(1)
    assert cache_lru.exists(3)
    assert cache_lru.size() == 2

def test_get_moves_to_front():
    cache_lru = LRUCache(3)
    cache_lru.put(1, 10)  # LRU: [1]
    cache_lru.put(2, 20)  # LRU: [1,2]
    cache_lru.put(3, 30)  # LRU: [1,2,3]

    # Access 1, it should move to front
    assert cache_lru.get(1) == 10  # Now LRU order: [2,3,1]

    # Add new item, 2 should be evicted (least recently used)
    cache_lru.put(4, 40)
    assert not cache_lru.exists(2)
    assert cache_lru.exists(1)
    assert cache_lru.exists(3)
    assert cache_lru.exists(4)
    assert cache_lru.size() == 3

def test_capacity_one_lru():
    cache_lru = LRUCache(1)
    cache_lru.put(1, 10)
    assert cache_lru.exists(1)
    assert cache_lru.get(1) == 10

    cache_lru.put(2, 20)  # Should evict 1
    assert not cache_lru.exists(1)
    assert cache_lru.exists(2)
    assert cache_lru.get(2) == 20
    assert cache_lru.size() == 1

def test_zero_capacity():
    cache_lru = LRUCache(0)
    assert cache_lru.size() == 0
    cache_lru.put(1, 10)  # Should not add anything
    assert cache_lru.size() == 0
    assert not cache_lru.exists(1)
    with pytest.raises(KeyError):
        cache_lru.get(1)

def test_keeps_all_values_within_capacity():
    cache_lru = LRUCache(TEST2_CACHE_CAPACITY)

    for i in range(NUM_OF_TEST2_RECORDS):
        cache_lru.put(i, i)

    for i in range(NUM_OF_TEST2_RECORDS - TEST2_CACHE_CAPACITY):
        assert not cache_lru.exists(i)

    for i in range(NUM_OF_TEST2_RECORDS - TEST2_CACHE_CAPACITY, NUM_OF_TEST2_RECORDS):
        assert cache_lru.exists(i)
        assert cache_lru.get(i) == i

    size = cache_lru.size()
    assert size == TEST2_CACHE_CAPACITY