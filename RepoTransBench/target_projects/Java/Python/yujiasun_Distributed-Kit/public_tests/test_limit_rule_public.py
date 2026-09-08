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

def test_getters_and_setters_public():
    rule = LimitRule()
    rule.setSeconds(25)
    rule.setLimitCount(12)
    rule.setLockCount(5)
    rule.setLockTime(200)
    assert rule.getSeconds() == 25
    assert rule.getLimitCount() == 12
    assert rule.getLockCount() == 5
    assert rule.getLockTime() == 200

def test_enable_limit_lock_false_when_zero_public():
    rule = LimitRule()
    rule.setLockTime(0)
    rule.setLockCount(0)
    assert not rule.enableLimitLock()

def test_enable_limit_lock_false_when_one_zero_public():
    rule = LimitRule()
    rule.setLockTime(8)
    rule.setLockCount(0)
    assert not rule.enableLimitLock()

    rule.setLockTime(0)
    rule.setLockCount(6)
    assert not rule.enableLimitLock()

def test_enable_limit_lock_true_public():
    rule = LimitRule()
    rule.setLockTime(15)
    rule.setLockCount(4)
    assert rule.enableLimitLock()