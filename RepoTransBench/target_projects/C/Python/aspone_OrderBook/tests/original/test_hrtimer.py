import pytest
from src.aspone_orderbook.hrtimer import HRTimer
import time

def test_hrtimer_basic():
    t = HRTimer()
    t.start()
    time.sleep(0.001) # 1 millisecond
    elapsed = t.stop()
    assert elapsed > 0
    # Allow for some minor timing inaccuracies (e.g., within 2ms of expected)
    # 1ms = 1_000_000 ns. Elapsed should be around this value.
    assert abs(elapsed - 1_000_000) < 2_000_000 # Allow up to 2ms deviation
    assert t.get_elapsed() == elapsed

def test_hrtimer_double_stop():
    t = HRTimer()
    t.start()
    time.sleep(0.0005) # 500 microseconds (0.5 milliseconds)
    first = t.stop()
    second = t.stop() # Should be 0
    assert first > 0
    assert second == 0
    assert t.get_elapsed() == first # get_elapsed should hold the first value

def test_hrtimer_no_start():
    t = HRTimer()
    elapsed = t.stop() # Should be 0
    assert elapsed == 0
    assert t.get_elapsed() == 0