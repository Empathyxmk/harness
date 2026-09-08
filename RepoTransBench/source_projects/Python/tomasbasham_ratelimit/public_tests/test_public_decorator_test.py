import pytest
import time
from ratelimit.decorators import RateLimitDecorator
from ratelimit.decorators import sleep_and_retry
from ratelimit.exception import RateLimitException

def test_public_simple_limit(monkeypatch):
    d = RateLimitDecorator(calls=3, period=0.04)
    # Allowed 3 times
    calls = []
    @d
    def myfun():
        calls.append(2)
        return sum(calls)
    assert myfun() == 2
    assert myfun() == 4
    assert myfun() == 6
    with pytest.raises(RateLimitException):
        myfun()
    time.sleep(0.045)
    assert myfun() == 8

def test_public_sleep_and_retry(monkeypatch):
    d = RateLimitDecorator(calls=1, period=0.02)
    @sleep_and_retry
    @d
    def fn():
        return 24
    assert fn() == 24
    t0 = time.time()
    assert fn() == 24
    assert time.time() - t0 >= 0.02

def test_public_raise_on_limit_false(monkeypatch):
    d = RateLimitDecorator(calls=1, period=0.03, raise_on_limit=False)
    track = []
    @d
    def fun():
        track.append(len(track)+1)
        return track[-1]
    assert fun() == 1
    assert fun() is None    # second call blocked, returns None
    time.sleep(0.035)
    assert fun() == 2