from datetime import datetime

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

def test_repeat_repeats_strings_as_expected_public():
    assert repeat('b', 4) == 'bbbb'
    assert repeat('=', 2) == '=='
    assert repeat('y', 0) == ''

def test_pad_pads_numbers_as_expected_public():
    assert pad(3, 4) == '0003'
    assert pad(77, 3) == '077'
    assert pad(120, 3) == '120'

def test_formatTime_returns_formatted_time_string_public():
    date = datetime(2022, 12, 25, 23, 59, 59, 99000)
    assert formatTime(date) == '23:59:59.099'

def test_timer_uses_performance_or_Date_public():
    assert isinstance(timer, Timer)
    assert callable(timer.now)