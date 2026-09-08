import pytest
from unittest.mock import MagicMock, patch
from types import MethodType

# Mocks for AccessSpeedLimit and LimitRule class interfaces
class LimitRule:
    def __init__(self):
        self._limit_count = 0
        self._seconds = 0
        self._lock_count = 0
        self._lock_time = 0

    def setLimitCount(self, val):
        self._limit_count = val
    def setSeconds(self, val):
        self._seconds = val
    def setLockCount(self, val):
        self._lock_count = val
    def setLockTime(self, val):
        self._lock_time = val
    def getLimitCount(self):
        return self._limit_count
    def getSeconds(self):
        return self._seconds
    def getLockCount(self):
        return self._lock_count
    def getLockTime(self):
        return self._lock_time
    def enableLimitLock(self):
        return self._lock_count > 0 and self._lock_time > 0

class AccessSpeedLimit:
    def __init__(self, jedis_pool=None):
        self._jedis_pool = jedis_pool
    def getJedisPool(self):
        return self._jedis_pool
    def setJedisPool(self, pool):
        self._jedis_pool = pool
    def tryAccess(self, key, seconds, limit):
        # Simulate Lua eval on Redis
        if hasattr(self, "_mock_result"):
            result = self._mock_result
            return str(result) not in ["0", "False"] and int(result) <= limit
        return False
    def buildLuaScript(self, rule):
        # Simulate logic based on LimitRule
        core = ""
        if rule.enableLimitLock():
            core += "redis.call('expire',KEYS[1],ARGV[4])"
        elif rule.getLockCount() == 0 and rule.getLockTime() == 0:
            core += "-- no ARGV[4]"
        return core

@pytest.fixture
def setup_access_limit():
    jedis_pool = MagicMock()
    jedis = MagicMock()
    jedis_pool.getResource.return_value = jedis
    asl = AccessSpeedLimit(jedis_pool=jedis_pool)
    return jedis_pool, jedis, asl

def test_get_set_jedis_pool():
    limit = AccessSpeedLimit()
    assert limit.getJedisPool() is None
    fake_pool = object()
    limit.setJedisPool(fake_pool)
    assert limit.getJedisPool() == fake_pool

def test_try_access_with_try_access_int(setup_access_limit):
    jedis_pool, jedis, asl = setup_access_limit
    asl._mock_result = "1"
    assert asl.tryAccess("keyX", 5, 3) == True

def test_try_access_false_returned(setup_access_limit):
    jedis_pool, jedis, asl = setup_access_limit
    asl._mock_result = "6"  # Simulate count higher than limit
    assert asl.tryAccess("keyZ", 10, 5) == False

def test_lua_script_includes_lock_logic():
    rule = LimitRule()
    rule.setLimitCount(5)
    rule.setSeconds(12)
    rule.setLockCount(6)
    rule.setLockTime(22)
    asl = AccessSpeedLimit()
    script = asl.buildLuaScript(rule)
    assert "redis.call('expire',KEYS[1],ARGV[4])" in script
    assert rule.enableLimitLock()

def test_lua_script_excludes_lock_logic():
    rule = LimitRule()
    rule.setLimitCount(7)
    rule.setSeconds(24)
    rule.setLockCount(0)
    rule.setLockTime(0)
    asl = AccessSpeedLimit()
    script = asl.buildLuaScript(rule)
    assert "ARGV[4]" not in script
    assert not rule.enableLimitLock()