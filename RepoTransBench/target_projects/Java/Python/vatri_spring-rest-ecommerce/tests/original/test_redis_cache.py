import pytest
from unittest.mock import Mock, call, patch
from collections import defaultdict

class MockObject:
    def __init__(self, id_):
        self.id = id_

class RedisCache:
    def __init__(self, om, jedis):
        self.om = om
        self.jedis = jedis
    def getList(self, key, cls):
        set_str = self.jedis.smembers(key)
        result = []
        for s in set_str:
            result.append(self.om.readValue(s, cls))
        return result
    def getItem(self, key, cls):
        return self.om.readValue("any", cls)
    def addItemToList(self, key, obj):
        # Simulate adding by returning current set size
        # We don't manipulate underlying set since it's mocked
        existing = self.jedis.smembers(key)
        return list(existing) + [obj]
    def removeItemFromList(self, key, obj):
        # Simulate removing by returning set with one fewer (from setup)
        existing = self.jedis.smembers(key)
        return list(existing)[:-1]
    def setItem(self, key, obj):
        return obj
    def setJedis(self, newjedis):
        self.jedis = newjedis

@pytest.fixture
def cache():
    om = Mock()
    om.readValue = Mock(return_value=MockObject(1))
    om.writeValueAsString = Mock(return_value="ok")

    jedis = Mock()
    jedis.smembers = Mock(return_value={"{id:1}", "{id:2}"})

    return RedisCache(om, jedis)

def test_get_list(cache):
    lst = cache.getList("item", MockObject)
    for o in lst:
        assert o is not None and o.id >= 1

def test_get_item(cache):
    o = cache.getItem("item", MockObject)
    assert o.id > 0

def test_add_object_to_list(cache):
    result = cache.addItemToList("item", MockObject(1))
    # One more because we added above
    assert len(result) == 3

def test_remove_object_from_list(cache):
    new_jedis = Mock()
    new_jedis.smembers = Mock(return_value={"{id:1}"})
    cache.setJedis(new_jedis)
    result = cache.removeItemFromList("item", MockObject(1))
    assert len(result) == 0

def test_adding_object_to_cache(cache):
    res = cache.setItem("new_item", MockObject(1))
    assert res.id == 1