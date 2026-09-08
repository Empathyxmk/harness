import pytest
import time
from ratelimit.decorators import RateLimitDecorator
from ratelimit.decorators import sleep_and_retry
from ratelimit.exception import RateLimitException

def test_public_negative_period(monkeypatch):
    # period < 0 should work as instant expiry, all calls allowed after window reset
    d = RateLimitDecorator(calls=1, period=-2)
    callcount = []
    @d
    def f():
        callcount.append(1)
        return 7
    assert f() == 7
    # Should raise, as period is negative (so resets instantly)
    with pytest.raises(RateLimitException):
        f()

def test_public_sleep_and_retry_succeeds(monkeypatch):
    rl = RateLimitDecorator(calls=1, period=0.02)
    call_times = []
    @sleep_and_retry
    @rl
    def fun():
        call_times.append(time.time())
        return 17
    assert fun() == 17
    # This call should trigger a rate limit sleep, then succeed
    t0 = time.time()
    res = fun()
    assert res == 17
    assert time.time() - t0 >= 0.02

def test_public_sleep_and_retry_multiple(monkeypatch):
    rl = RateLimitDecorator(calls=2, period=0.015)
    counter = {'count': 0}
    @sleep_and_retry
    @rl
    def g():
        counter['count'] += 2
        return counter['count']
    assert g() == 2
    assert g() == 4
    # Next call should be rate limited and sleep, then succeed
    t0 = time.time()
    val = g()
    assert val == 6
    assert counter['count'] == 6
    assert time.time() - t0 >= 0.015