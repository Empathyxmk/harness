import pytest
import sys
from ratelimit.decorators import RateLimitDecorator

def test_clamped_calls_min_and_max(monkeypatch):
    # calls < 1 clamps to 1
    d = RateLimitDecorator(calls=-9, period=1, clock=lambda: 0)
    assert d.clamped_calls == 1

    # calls > sys.maxsize clamps to sys.maxsize
    d2 = RateLimitDecorator(calls=sys.maxsize + 123456, period=1, clock=lambda: 0)
    assert d2.clamped_calls == sys.maxsize

def test_decorator_thread_safety():
    import threading
    result = []
    dec = RateLimitDecorator(calls=2, period=1, clock=lambda: 0)
    @dec
    def foo(x):
        result.append(x)
        return x

    t1 = threading.Thread(target=foo, args=(1,))
    t2 = threading.Thread(target=foo, args=(2,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    assert sorted(result) == [1, 2]

def test_period_remaining_zero(monkeypatch):
    # Cover logic for period_remaining == 0 branch
    state = {'reset':10}
    def fake_clock():
        return 20
    dec = RateLimitDecorator(calls=2, period=5, clock=fake_clock)
    dec.last_reset = 15
    # 20-15=5, period=5, remaining=0, should reset
    called = []
    @dec
    def f():
        called.append("called")
        return 123
    assert f() == 123
    # Call again, still works
    assert f() == 123

def test_period_remaining_negative(monkeypatch):
    # Test when period_remaining < 0 triggers window reset
    state = {'t': 0}
    def fake_clock():
        val = state['t']
        state['t'] += 100  # move clock forward fast
        return val
    dec = RateLimitDecorator(calls=1, period=1, clock=fake_clock)
    called = []
    @dec
    def foo():
        called.append(1)
    foo()
    foo()  # should reset after period_remaining < 0
    assert len(called) == 2