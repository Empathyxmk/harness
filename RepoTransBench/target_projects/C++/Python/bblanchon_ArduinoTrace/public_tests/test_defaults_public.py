import pytest
from arduinotrace.trace import TRACE

def test_trace_multiple_default_does_not_crash():
    # Use TRACE multiple times: should not crash
    TRACE()
    TRACE()