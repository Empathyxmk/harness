import pytest
from arduinotrace.trace import TRACE, Serial

def test_trace_disabled_public(monkeypatch):
    # Simulate ARDUINOTRACE_ENABLE 0 by making TRACE a noop
    monkeypatch.setattr('arduinotrace.trace.TRACE', lambda: None)
    Serial.clear()
    TRACE()
    TRACE()
    assert Serial.get_output() == []