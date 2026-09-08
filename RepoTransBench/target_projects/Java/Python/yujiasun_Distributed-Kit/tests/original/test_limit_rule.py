class LimitRule:
    def __init__(self):
        self._limit_count = 0
        self._seconds = 0
        self._lock_count = 0
        self._lock_time = 0

    def setSeconds(self, val):
        self._seconds = val
    def setLimitCount(self, val):
        self._limit_count = val
    def setLockCount(self, val):
        self._lock_count = val
    def setLockTime(self, val):
        self._lock_time = val
    def getSeconds(self):
        return self._seconds
    def getLimitCount(self):
        return self._limit_count
    def getLockCount(self):
        return self._lock_count
    def getLockTime(self):
        return self._lock_time
    def enableLimitLock(self):
        return self._lock_time > 0 and self._lock_count > 0

def test_getters_and_setters():
    rule = LimitRule()
    rule.setSeconds(15)
    rule.setLimitCount(10)
    rule.setLockCount(3)
    rule.setLockTime(120)
    assert rule.getSeconds() == 15
    assert rule.getLimitCount() == 10
    assert rule.getLockCount() == 3
    assert rule.getLockTime() == 120

def test_enable_limit_lock_false_when_zero():
    rule = LimitRule()
    rule.setLockTime(0)
    rule.setLockCount(0)
    assert not rule.enableLimitLock()

def test_enable_limit_lock_false_when_one_zero():
    rule = LimitRule()
    rule.setLockTime(5)
    rule.setLockCount(0)
    assert not rule.enableLimitLock()

    rule.setLockTime(0)
    rule.setLockCount(5)
    assert not rule.enableLimitLock()

def test_enable_limit_lock_true():
    rule = LimitRule()
    rule.setLockTime(10)
    rule.setLockCount(3)
    assert rule.enableLimitLock()