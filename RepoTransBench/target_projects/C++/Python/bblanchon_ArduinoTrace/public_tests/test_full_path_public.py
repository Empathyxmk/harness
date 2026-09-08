import pytest
from arduinotrace.trace import TRACE, Serial

def test_trace_basic_api_public():
    # Basic API usage test, call twice for coverage
    Serial.clear()
    TRACE()
    TRACE()
    output = Serial.get_output()
    # There should be two "TRACE: called" logs
    assert sum("TRACE: called" in l for l in output) == 2