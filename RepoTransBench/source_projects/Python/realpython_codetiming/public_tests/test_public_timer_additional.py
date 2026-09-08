import math
import pytest
from codetiming._timer import Timer, TimerError

def test_timer_context_manager_runs_public():
    timer = Timer("public_cmmsg", text="Public elapsed: {0:.6f}s")
    with timer:
        x = 42  # Public flavor, just in context

def test_timer_start_stop_elapsed_public():
    timer = Timer("public_simple", text="Duration {0:.2f}")
    assert timer._start_time is None
    timer.start()
    assert timer._start_time is not None
    timer.stop()
    elapsed = timer.last
    assert isinstance(elapsed, float)
    assert elapsed >= 0.0

def test_timer_str_repr_public():
    timer = Timer("public_simple", text="Duration {0:.2f}")
    assert isinstance(str(timer), str)
    assert "Timer" in repr(timer)

def test_timer_running_status_via_private_public():
    timer = Timer("public_runstat", text="Now running:{0}")
    timer.start()
    assert timer._start_time is not None
    timer.stop()
    assert timer._start_time is None

def test_timer_logger_callable_text_public():
    messages = []
    def logger_fn(msg): messages.append(msg)
    timer = Timer("public_cbmsg", text=lambda s: f"Elapsed={s:.3f}", logger=logger_fn)
    timer.start()
    timer.stop()
    assert messages
    assert "Elapsed=" in messages[0]

def test_timer_without_text_logger_public():
    timer = Timer("public_notext", text=None, logger=None)
    timer.start()
    timer.stop()  # Should succeed without output or error

def test_timer_stop_without_start_raises_public():
    timer = Timer("public_exception", text="fail fast")
    with pytest.raises(TimerError):
        timer.stop()

def test_timer_multiple_starts_raises_public():
    timer = Timer("public_multi", text="multi-case")
    timer.start()
    with pytest.raises(TimerError):
        timer.start()
    timer.stop()

def test_timer_last_when_nan_public():
    timer = Timer("public_none", text="noneCase")
    assert math.isnan(timer.last)

def test_timer_compare_multiple_instances_public():
    timer1 = Timer("public_x")
    timer2 = Timer("public_y")
    assert timer1 is not timer2