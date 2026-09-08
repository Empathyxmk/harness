import pytest
from arduinotrace.trace import TRACE

def test_trace_default_does_not_crash():
    # Ensure the default configuration does not crash
    # No assertion needed (should not raise)
    TRACE()