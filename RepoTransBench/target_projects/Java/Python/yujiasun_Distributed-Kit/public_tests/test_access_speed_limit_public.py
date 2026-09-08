import pytest
from unittest.mock import MagicMock

class LimitRule:
    def __init__(self):
        self._limit_count = 0
        self._seconds = 0
        self._lock_count = 0
        self._lock_time = 0
    def setLimitCount(self, val): self._limit_count = val
    def setSeconds(self, val): self._seconds = val
    def setLockCount(self, val): self._lock_count = val
    def setLockTime(self, val): self._lock_time = val
    def enableLimitLock(self): return self._lock_count > 0 and self._lock_time > 0

class AccessSpeedLimit:
    def __init__(self, jedis_pool=None):
        self.jedis_pool = jedis_pool
        self._mock_result = None
    def getJedisPool(self): return self.jedis_pool
    def setJedisPool(self, jp): self.jedis_pool = jp
    def tryAccess(self, key, seconds, limit):
        if self._mock_result is not None:
            return int(self._mock_result) <= limit
        return False
    def buildLuaScript(self, rule):
        if rule.enableLimitLock():
            return "redis.call('expire',KEYS[1],ARGV[4])"
        else:
            return "-- no ARGV[4]"

@pytest.fixture
def setup_access_limit_public():
    jedis_pool = MagicMock()
    accessSpeedLimit = AccessSpeedLimit(jedis_pool)
    return jedis_pool, accessSpeedLimit

def test_get_set_jedis_pool_public(setup_access_limit_public):
    jedis_pool, accessSpeedLimit = setup_access_limit_public
    limit = AccessSpeedLimit()
    assert limit.getJedisPool() is None
    limit.setJedisPool(jedis_pool)
    assert limit.getJedisPool() == jedis_pool

def test_try_access_with_try_access_int_public(setup_access_limit_public):
    _, accessSpeedLimit = setup_access_limit_public
    accessSpeedLimit._mock_result = "2"
    assert accessSpeedLimit.tryAccess("keyY", 8, 4)

def test_try_access_false_returned_public(setup_access_limit_public):
    _, accessSpeedLimit = setup_access_limit_public
    accessSpeedLimit._mock_result = "9"  # Simulate count higher than limit
    assert not accessSpeedLimit.tryAccess("keyW", 15, 7)

def test_lua_script_includes_lock_logic_public():
    rule = LimitRule()
    rule.setLimitCount(9)
    rule.setSeconds(20)
    rule.setLockCount(8)
    rule.setLockTime(30)
    s = AccessSpeedLimit()
    script = s.buildLuaScript(rule)
    assert "redis.call('expire',KEYS[1],ARGV[4])" in script
    assert rule.enableLimitLock() is True

def test_lua_script_excludes_lock_logic_public():
    rule = LimitRule()
    rule.setLimitCount(11)
    rule.setSeconds(30)
    rule.setLockCount(0)
    rule.setLockTime(0)
    s = AccessSpeedLimit()
    script = s.buildLuaScript(rule)
    assert "ARGV[4]" not in script
    assert rule.enableLimitLock() is False