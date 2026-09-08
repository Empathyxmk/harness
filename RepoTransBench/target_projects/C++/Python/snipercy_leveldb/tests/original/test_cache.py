def test_cache_simple_lru():
    cache = {}
    cache[100] = 101
    assert cache[100] == 101
    cache[200] = 201
    assert cache[100] == 101
    assert cache[200] == 201
    cache[100] = 102
    assert cache[100] == 102
    del cache[100]
    assert 100 not in cache

def test_cache_eviction_policy():
    cache = {}
    for i in range(1100):
        cache[i] = 1000 + i
    for i in range(1100):
        assert cache[i] == 1000 + i

def test_cache_new_id():
    import uuid
    id1 = uuid.uuid4()
    id2 = uuid.uuid4()
    assert id1 != id2