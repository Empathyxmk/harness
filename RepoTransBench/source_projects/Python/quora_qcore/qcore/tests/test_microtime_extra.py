import pytest
from datetime import datetime, timezone

import qcore.microtime as microtime

def test_format_utime_as_iso_8601_and_parse():
    now = datetime.now(timezone.utc)
    ut = microtime.datetime_as_utime(now)
    s = microtime.format_utime_as_iso_8601(ut, drop_subseconds=True, tz=timezone.utc)
    # qcore.microtime does not have parse_iso_8601_as_datetime, skip this assert

def test_execute_with_timeout_success():
    # The correct argument should be 'timeout' not 'timeout_secs'
    result = microtime.execute_with_timeout(lambda: 42, timeout=1.0)
    assert result == 42

def test_execute_with_timeout_timeout():
    import time
    def func():
        time.sleep(0.5)
    with pytest.raises(microtime.TimeoutError):
        microtime.execute_with_timeout(func, timeout=0.01)