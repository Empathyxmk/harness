import time
import threading
import pytest

from src.Timer import Timer

def test_clear_interval_on_stop_different_value():
    timer = Timer(15)
    assert timer.timer is not None
    timer.stop()
    assert timer.timer is None

def test_restart_timer_with_start_different_delay():
    timer = Timer(8)
    timer.stop()
    assert timer.timer is None
    timer.start()
    time.sleep(0.02)
    assert timer.timer is not None
    timer.stop()

def test_emit_step_multiple_times():
    timer = Timer(3)
    call_count = {'count': 0}
    max_calls = 2
    def cb():
        call_count['count'] += 1
        if call_count['count'] >= max_calls:
            timer.stop()
            assert call_count['count'] == max_calls
    timer.on('step', cb)
    # Sleep enough time for both steps to occur (assume step is about every 3ms)
    time.sleep(0.02)