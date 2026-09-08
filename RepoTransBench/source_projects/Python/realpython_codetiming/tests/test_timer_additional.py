import math
import pytest
from codetiming._timer import Timer, TimerError

def test_timer_context_manager_runs():
    timer = Timer("cmmsg", text="Elapsed time: {0:.4f}s")
    with timer:
        pass  # just check context manager works

def test_timer_start_stop_elapsed():
    timer = Timer("simple", text="Time {0:.4f}")
    assert timer._start_time is None
    timer.start()
    assert timer._start_time is not None
    timer.stop()
    elapsed = timer.last
    assert isinstance(elapsed, float)

def test_timer_str_repr():
    timer = Timer("simple", text="Time {0:.4f}")
    assert isinstance(str(timer), str)
    assert "Timer" in repr(timer)

def test_timer_running_status_via_private():
    timer = Timer("runstat", text="Running:{0}")
    timer.start()
    assert timer._start_time is not None
    timer.stop()
    assert timer._start_time is None

def test_timer_logger_callable_text():
    messages = []
    timer = Timer("cbmsg", text=lambda s: f"Time={s:.2f}", logger=messages.append)
    timer.start()
    timer.stop()
    assert messages
    assert "Time=" in messages[0]

def test_timer_without_text_logger():
    timer = Timer("notext", text=None, logger=None)
    timer.start()
    timer.stop()  # Should simply not log or raise

def test_timer_stop_without_start_raises():
    timer = Timer("exception", text="fail")
    # Calling stop before start should raise TimerError
    with pytest.raises(TimerError):
        timer.stop()

def test_timer_multiple_starts_raises():
    timer = Timer("multi", text="multi")
    timer.start()
    with pytest.raises(TimerError):
        timer.start()
    timer.stop()

def test_timer_last_when_nan():
    timer = Timer("none", text="none")
    # Should return nan if never stopped
    assert math.isnan(timer.last)

def test_timer_compare_multiple_instances():
    timer1 = Timer("a")
    timer2 = Timer("b")
    assert timer1 is not timer2