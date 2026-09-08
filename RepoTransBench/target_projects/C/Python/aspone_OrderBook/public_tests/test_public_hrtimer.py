import pytest
from src.aspone_orderbook.hrtimer import HRTimer
import time

def test_public_hrtimer_basic():
    t = HRTimer()
    t.start()
    time.sleep(0.003) # 3 milliseconds, different from original 1ms
    elapsed = t.stop()
    assert elapsed > 0
    assert abs(elapsed - 3_000_000) < 2_000_000 # Allow up to 2ms deviation
    assert t.get_elapsed() == elapsed

def test_public_hrtimer_double_stop():
    t = HRTimer()
    t.start()
    time.sleep(0.002) # 2 milliseconds, different from original 500us
    first = t.stop()
    second = t.stop() # Should be 0
    assert first > 0
    assert second == 0
    assert t.get_elapsed() == first

def test_public_hrtimer_no_start():
    t = HRTimer()
    elapsed = t.stop() # Should be 0
    assert elapsed == 0
    assert t.get_elapsed() == 0