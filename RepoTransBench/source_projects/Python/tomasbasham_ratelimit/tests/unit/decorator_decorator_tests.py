import pytest
import time

from ratelimit.decorators import RateLimitDecorator, sleep_and_retry
from ratelimit.exception import RateLimitException

def dummy_clock():
    # Start at 1000, increments by 1 on each call
    state = {'value': 1000}
    def _clock():
        val = state['value']
        state['value'] += 1
        return val
    return _clock

def test_decorator_allows_calls_within_limit():
    calls = []
    clock = dummy_clock()
    @RateLimitDecorator(calls=2, period=10, clock=clock)
    def func(x):
        calls.append(x)
        return x
    assert func(2) == 2
    assert func(3) == 3
    # Within limit, calls list should have two
    assert calls == [2, 3]

def test_decorator_raises_on_exceeding_limit():
    clock = dummy_clock()
    decorated_calls = []
    @RateLimitDecorator(calls=1, period=10, clock=clock, raise_on_limit=True)
    def func(x):
        decorated_calls.append(x)
        return x
    func(1)
    with pytest.raises(RateLimitException) as exc:
        func(2)
    assert "too many calls" in str(exc.value)
    assert exc.value.period_remaining == 9

def test_decorator_returns_none_when_raise_on_limit_false():
    clock = dummy_clock()
    calls = []
    @RateLimitDecorator(calls=1, period=10, clock=clock, raise_on_limit=False)
    def func(x):
        calls.append(x)
        return x
    assert func(5) == 5
    assert func(6) is None
    assert calls == [5]

def test_decorator_resets_after_period(monkeypatch):
    # Start clock at 0, increments by .1 per call
    state = {'t': 0.0}
    def fake_clock():
        val = state['t']
        state['t'] += .1
        return val

    @RateLimitDecorator(calls=1, period=0.05, clock=fake_clock)
    def f(x):
        return x

    # Call 1st time
    assert f(1) == 1
    # Advances clock, so period remaining negative, resets etc.
    assert f(2) == 2

def test_sleep_and_retry_sleeps_and_retries(monkeypatch):
    call_count = {'count': 0}
    sleep_periods = []
    def fake_sleep(p):
        sleep_periods.append(p)

    class Exc(RateLimitException):
        pass

    def always_fail(*args, **kwargs):
        # Fail once, then succeed.
        if call_count['count'] == 0:
            call_count['count'] += 1
            raise RateLimitException('too many', 0.01)
        return "worked!"

    monkeypatch.setattr(time, "sleep", fake_sleep)
    decorated = sleep_and_retry(always_fail)
    result = decorated()
    assert result == "worked!"
    assert sleep_periods == [0.01]

def test_period_remaining_returns_proper_value():
    state = {'t': 500, 'reset': 498}
    def fake_clock():
        return state['t']
    dec = RateLimitDecorator(calls=1, period=10, clock=fake_clock)
    dec.last_reset = state['reset']
    state['t'] = 505
    remaining = dec._RateLimitDecorator__period_remaining()
    # period is 10, elapsed 505-498=7, remaining 3
    assert remaining == 3