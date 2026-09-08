import pytest
from unittest.mock import Mock
import json

class RedisCache:
    def __init__(self, om, jedis):
        self.om = om
        self.jedis = jedis
    def set(self, key, value):
        val = json.dumps(value)
        resp = self.jedis.set(key, val)
        return resp == "OK"
    def get(self, key, cls):
        if self.jedis.exists(key):
            val = self.jedis.get(key)
            # simulate objectmapper - loads from json string
            return json.loads(val)
        return None
    def delete(self, key):
        return self.jedis.del_(key) > 0

def test_set_and_get_different_key_value():
    om = object()
    jedis = Mock()
    key = "publicKey"
    value = "publicValue"
    jsonValue = json.dumps(value)
    jedis.set.return_value = "OK"
    jedis.get.return_value = jsonValue
    jedis.exists.side_effect = lambda k: (k == key)
    cache = RedisCache(om, jedis)
    assert cache.set(key, value)
    retrieved = cache.get(key, str)
    assert retrieved == value
    jedis.exists.side_effect = lambda k: False
    assert cache.get("missingKey", str) is None

def test_delete_key():
    om = object()
    jedis = Mock()
    key = "deletePublic"
    jedis.del_ = Mock(return_value=1)
    cache = RedisCache(om, jedis)
    assert cache.delete(key)
    jedis.del_.return_value = 0
    assert not cache.delete("doesNotExist")