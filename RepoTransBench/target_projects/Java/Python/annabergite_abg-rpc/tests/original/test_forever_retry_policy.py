import pytest

class RetrySleeper:
    def __call__(self, time, unit):
        pass

class ForeverRetryPolicy:
    def __init__(self, n, sleep_ms):
        if n < 0:
            raise ValueError("n must be >= 0")
        if sleep_ms <= 0:
            raise ValueError("sleep_ms must be > 0")
        if n > 50 and sleep_ms < 20:
            raise ValueError("bad config")
        self.n = n
        self.sleep_ms = sleep_ms

    def allow_retry(self, retry_count, elapsed_time_ms, sleeper):
        try:
            sleeper(retry_count, elapsed_time_ms)
            return True
        except InterruptedError:
            return False

def test_constructor_and_allow_valid():
    policy = ForeverRetryPolicy(10, 100)
    assert policy is not None
    sleeper = lambda time, unit: None
    assert policy.allow_retry(0, 0, sleeper)
    assert policy.allow_retry(5, 0, sleeper)
    assert policy.allow_retry(-1, 0, sleeper)

def test_allow_retry_interrupted():
    policy = ForeverRetryPolicy(10, 100)
    def broken_sleeper(time, unit):
        raise InterruptedError()
    assert not policy.allow_retry(0, 0, broken_sleeper)

def test_constructor_invalid_arguments():
    with pytest.raises(ValueError):
        ForeverRetryPolicy(-1, 10)
    with pytest.raises(ValueError):
        ForeverRetryPolicy(1, 0)
    with pytest.raises(ValueError):
        ForeverRetryPolicy(100, 10)