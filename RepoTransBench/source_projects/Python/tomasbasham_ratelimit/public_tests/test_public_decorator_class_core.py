import pytest
import time
from ratelimit.decorators import RateLimitDecorator
from ratelimit.exception import RateLimitException

def test_public_constructor_clamps_calls(monkeypatch):
    # Test with 0
    rld = RateLimitDecorator(calls=0, period=2)
    assert rld.clamped_calls == 1
    # Test with a very large positive number (variance from original)
    import sys
    rld = RateLimitDecorator(calls=sys.maxsize + 100, period=2)
    assert rld.clamped_calls == sys.maxsize
    # Test with non-integer just above int boundary
    rld = RateLimitDecorator(calls=7.8, period=2)
    assert rld.clamped_calls == 7

def test_public_decorator_rate_limit_raises(monkeypatch):
    rl = RateLimitDecorator(calls=2, period=0.03)
    @rl
    def foo():
        return "bar"
    assert foo() == "bar"
    assert foo() == "bar"
    with pytest.raises(RateLimitException):
        foo()
    # Wait for reset
    time.sleep(0.035)
    assert foo() == "bar"

def test_public_decorator_does_not_raise(monkeypatch):
    rl = RateLimitDecorator(calls=2, period=0.04, raise_on_limit=False)
    result = []
    @rl
    def bar():
        result.append('x')
        return len(result)
    assert bar() == 1
    assert bar() == 2
    time.sleep(0.045)  # past period so next call starts new cycle
    assert bar() == 3

def test_public_thread_safety():
    rld = RateLimitDecorator(calls=4, period=1)
    # Lock creation check; call more times to trigger lock use
    def dummy2():
        return 24
    wrapped = rld(dummy2)
    for _ in range(3):
        wrapped()
    # After several calls, lock attribute should exist
    assert any('lock' in attr for attr in rld.__dict__)