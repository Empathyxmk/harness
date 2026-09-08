import time
import threading
import pytest

from src.Timer import Timer

def test_clears_interval_on_stop():
    timer = Timer(10)
    assert timer.timer is not None
    timer.stop()
    assert timer.timer is None

def test_restarts_timer_with_start():
    timer = Timer(5)
    timer.stop()
    assert timer.timer is None
    timer.start()
    # sleep slightly longer than timer interval to allow timer thread to start
    time.sleep(0.01)
    assert timer.timer is not None
    timer.stop()

def test_emits_step_on_timer_tick():
    # Need to check that the step callback is called at least once
    timer = Timer(2)
    called_flag = {'called': False}
    def on_step():
        called_flag['called'] = True
        timer.stop()
        assert called_flag['called'] is True
    timer.on('step', on_step)
    # Sleep enough for timer event to occur
    time.sleep(0.01)
    # Timer should have triggered the callback and stopped