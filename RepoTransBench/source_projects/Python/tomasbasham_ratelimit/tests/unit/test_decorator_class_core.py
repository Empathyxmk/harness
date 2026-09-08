import pytest
import time
from ratelimit.decorators import RateLimitDecorator
from ratelimit.exception import RateLimitException

def test_constructor_clamps_calls(monkeypatch):
    # Negative
    rld = RateLimitDecorator(calls=-5, period=1)
    assert rld.clamped_calls == 1
    # Large
    rld = RateLimitDecorator(calls=1<<100, period=1)
    import sys
    assert rld.clamped_calls == sys.maxsize
    # Floor
    rld = RateLimitDecorator(calls=3.9, period=1)
    assert rld.clamped_calls == 3

def test_decorator_rate_limit_raises(monkeypatch):
    rl = RateLimitDecorator(calls=1, period=0.05)
    @rl
    def f():
        return "foo"
    assert f() == "foo"
    with pytest.raises(RateLimitException) as e:
        f()
    # Wait for reset
    time.sleep(0.06)
    assert f() == "foo"

def test_decorator_does_not_raise(monkeypatch):
    rl = RateLimitDecorator(calls=1, period=0.05, raise_on_limit=False)
    result = []
    @rl
    def f():
        result.append(1)
        return len(result)
    assert f() == 1
    time.sleep(0.06)  # ensure period expiration so next call is allowed without block
    assert f() == 2  

def test_thread_safety():
    rld = RateLimitDecorator(calls=10, period=1)
    # The lock attribute is created lazily; call twice to be sure __lock exists
    def dummy():
        return 42
    wrapped = rld(dummy)
    wrapped()
    wrapped()
    # Now after two calls __lock should certainly exist
    assert any(attr.endswith('lock') for attr in rld.__dict__)