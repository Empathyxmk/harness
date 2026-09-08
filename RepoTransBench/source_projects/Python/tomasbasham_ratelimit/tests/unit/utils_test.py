import types
import time
from ratelimit.utils import now

def test_now_returns_callable_and_returns_float():
    monotonic_or_time = now()
    assert callable(monotonic_or_time)
    value = monotonic_or_time()
    assert isinstance(value, float)

def test_now_fallback(monkeypatch):
    monkeypatch.delattr(time, "monotonic", raising=False)
    fn = now()
    assert callable(fn)
    # Should fallback to time.time
    assert abs(fn() - time.time()) < 1.0