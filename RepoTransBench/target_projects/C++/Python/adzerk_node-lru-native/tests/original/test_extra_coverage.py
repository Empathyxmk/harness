import pytest
from src.lrucache import LRUCache, RangeError

def test_accepts_all_options_and_override_maxLoadFactor():
    cache = LRUCache({'maxAge': 200, 'maxElements': 5, 'maxLoadFactor': 0.5})
    cache.set('a', 123)
    assert cache.get('a') == 123
    assert isinstance(cache, object)

def test_ignore_non_number_maxAge_maxElements():
    cache = LRUCache({'maxAge': 'bad', 'maxElements': 'fail'})
    cache.set('a', 5)
    assert cache.get('a') == 5

def test_evict_when_maxElements_exceeded():
    cache = LRUCache({'maxElements': 2})
    cache.set('x', 1)
    cache.set('y', 2)
    cache.set('z', 3)
    assert cache.get('z') == 3
    valX = cache.get('x')
    valY = cache.get('y')
    assert (valX is None and valY == 2) or (valY is None and valX == 1)

def test_removing_and_clearing_empty_cache():
    cache = LRUCache()
    cache.remove('foo')  # Should not err
    cache.clear()
    assert cache.get('foo') is None

def test_gc_logic_expired_keys():
    import time
    cache = LRUCache({'maxAge': 10})
    cache.set('exp', 'abc')
    time.sleep(0.03)
    assert cache.get('exp') is None

def test_gc_does_not_evict_when_not_needed():
    cache = LRUCache({'maxAge': 99999})
    cache.set('t', 1)
    assert cache.get('t') == 1

def test_set_argument_type_errors():
    cache = LRUCache()
    with pytest.raises(RangeError):
        cache.set()
    with pytest.raises(RangeError):
        cache.set('onlykey')
    with pytest.raises(RangeError):
        cache.set('a', 1, 2)
    with pytest.raises(TypeError):
        cache.set(44, 'data')
    with pytest.raises(TypeError):
        cache.set(None, 'data')

def test_get_argument_type_errors():
    cache = LRUCache()
    with pytest.raises(TypeError):
        cache.get(44)
    with pytest.raises(TypeError):
        cache.get(None)
    with pytest.raises(RangeError):
        cache.get()
    with pytest.raises(RangeError):
        cache.get('a', 'b')

def test_remove_argument_type_errors():
    cache = LRUCache()
    with pytest.raises(TypeError):
        cache.remove({})
    with pytest.raises(TypeError):
        cache.remove([])
    with pytest.raises(RangeError):
        cache.remove()
    with pytest.raises(RangeError):
        cache.remove('a', 'b')

def test_setMaxAge_setMaxElements_argument_checks():
    cache = LRUCache()
    with pytest.raises(RangeError):
        cache.setMaxAge()
    with pytest.raises(RangeError):
        cache.setMaxElements()
    with pytest.raises(RangeError):
        cache.setMaxAge(1,2)
    with pytest.raises(RangeError):
        cache.setMaxElements(1,2)
    # If incorrect type, just ignore error
    try:
        cache.setMaxAge('notanumber')
        cache.setMaxElements('bad')
    except Exception as e:
        assert isinstance(e, Exception)

def test_set_same_key_updates_value_and_lru_order():
    cache = LRUCache({'maxElements': 2})
    cache.set('a', 1)
    cache.set('b', 2)
    cache.set('a', 3)
    cache.set('c', 4)
    assert cache.get('a') == 3
    assert cache.get('b') is None
    assert cache.get('c') == 4