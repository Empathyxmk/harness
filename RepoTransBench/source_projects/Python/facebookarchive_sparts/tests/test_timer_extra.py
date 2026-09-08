from sparts.timer import Timer
import time

def test_timer_basic_and_elapsed():
    t = Timer()
    time.sleep(0.01)
    elapsed1 = t.elapsed
    assert elapsed1 > 0
    t.start()
    time.sleep(0.01)
    elapsed2 = t.elapsed
    assert elapsed2 > elapsed1

def test_timer_str_and_repr():
    t = Timer()
    out = str(t)
    assert "Timer" in out
    reprout = repr(t)
    assert "Timer" in reprout