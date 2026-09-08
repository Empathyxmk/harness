from datetime import datetime
import pytest

def repeat(s, n):
    return s * n

def pad(num, width):
    s = str(num)
    return s.zfill(width)

def formatTime(date):
    return date.strftime('%H:%M:%S.') + pad(date.microsecond // 1000, 3)

class Timer:
    @staticmethod
    def now():
        import time
        return time.time() * 1000

timer = Timer()

def test_repeat_repeats_strings_as_expected():
    assert repeat('a', 3) == 'aaa'
    assert repeat('-', 0) == ''
    assert repeat('x', 1) == 'x'

def test_pad_pads_numbers_as_expected():
    assert pad(5, 2) == '05'
    assert pad(15, 2) == '15'
    assert pad(7, 3) == '007'

def test_formatTime_returns_formatted_time_string():
    date = datetime(2000, 1, 1, 9, 5, 2, 8000)
    assert formatTime(date) == '09:05:02.008'

def test_timer_uses_performance_or_Date():
    assert isinstance(timer, Timer)
    assert callable(timer.now)