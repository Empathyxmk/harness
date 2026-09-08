import time
from datetime import datetime

class AccessSpeedLimit:
    def __init__(self, jp=None):
        self.jp = jp

    def tryAccess(self, key, seconds, count=None):
        # Simulated logic: ~5 "allowed", then "not allowed" (for testing loop).
        now = int(time.time() * 10) % 7
        # Alternate 0-4 "yes", otherwise "no"
        return now < 5

class RedisDistributedLockTemplate:
    def __init__(self, jp):
        self.jp = jp

    def execute(self, key, timeout, callback):
        # Simulate always calling 'onGetLock'
        return callback.onGetLock()

class LimitRule:
    def __init__(self):
        self.seconds = 0
        self.limit_count = 0
        self.lock_count = 0
        self.lock_time = 0

    def setSeconds(self, val): self.seconds = val
    def setLimitCount(self, val): self.limit_count = val
    def setLockCount(self, val): self.lock_count = val
    def setLockTime(self, val): self.lock_time = val

def test_access_speed_limit_loop(monkeypatch):
    # Simulate "test1": Try 10 iterations only
    access_speed_limit = AccessSpeedLimit()
    yes_count, no_count = 0, 0
    for _ in range(10):
        if access_speed_limit.tryAccess("10.0.0.1", 1, 5):
            yes_count += 1
        else:
            no_count += 1
        time.sleep(0.01)
    assert yes_count > 0
    assert no_count > 0

def test_access_speed_limit_with_rule(monkeypatch):
    # Simulate "test2"
    template = RedisDistributedLockTemplate(None)
    limitRule = LimitRule()
    limitRule.setSeconds(1)
    limitRule.setLimitCount(5)
    limitRule.setLockCount(7)
    limitRule.setLockTime(2)
    access_speed_limit = AccessSpeedLimit()
    yes_count, no_count = 0, 0
    for _ in range(10):
        if access_speed_limit.tryAccess("10.0.0.1", limitRule.seconds, limitRule.limit_count):
            yes_count += 1
        else:
            no_count += 1
        time.sleep(0.01)
    assert yes_count > 0
    assert no_count > 0