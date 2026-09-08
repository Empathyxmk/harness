import pytest
from src.lrucache import LRUCache, RangeError

@pytest.fixture
def cache():
    return LRUCache()

def test_get_no_arguments_throws_rangeerror(cache):
    with pytest.raises(RangeError):
        cache.get()

def test_get_two_arguments_throws_rangeerror(cache):
    with pytest.raises(RangeError):
        cache.get("foo", "bar")

def test_set_no_arguments_throws_rangeerror(cache):
    with pytest.raises(RangeError):
        cache.set()

def test_set_one_argument_throws_rangeerror(cache):
    with pytest.raises(RangeError):
        cache.set("foo")

def test_set_three_arguments_throws_rangeerror(cache):
    with pytest.raises(RangeError):
        cache.set("foo", "bar", "baz")

def test_remove_no_arguments_throws_rangeerror(cache):
    with pytest.raises(RangeError):
        cache.remove()

def test_remove_two_arguments_throws_rangeerror(cache):
    with pytest.raises(RangeError):
        cache.remove("foo", "bar")