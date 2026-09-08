import pytest
import time
import ratelimit.utils

def test_now_returns_monotonic_or_time(monkeypatch):
    # Test when time has monotonic
    func = ratelimit.utils.now()
    assert callable(func)
    t1 = func()
    time.sleep(0.01)
    t2 = func()
    assert t2 > t1

    # Test fallback to time.time if monotonic not present
    monkeypatch.setattr(time, "monotonic", None, raising=False)
    monkeypatch.delattr(time, "monotonic", raising=False)
    func = ratelimit.utils.now()
    t1 = func()
    time.sleep(0.01)
    t2 = func()
    assert t2 > t1