import pytest
from arduinotrace.trace import TRACE, Serial

def test_trace_basic_api_usage():
    # Basic API usage test
    Serial.clear()
    TRACE()
    # In this mockup, check the Serial has output
    assert any("TRACE: called" in l for l in Serial.get_output())