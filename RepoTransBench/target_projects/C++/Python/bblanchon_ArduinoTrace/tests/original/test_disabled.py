import pytest
from arduinotrace.trace import TRACE, Serial

def test_trace_disabled(monkeypatch):
    # Simulate tracing being disabled: In practice, TRACE would do nothing
    # We'll monkeypatch TRACE to a noop for this test to simulate ARDUINOTRACE_ENABLE=0
    monkeypatch.setattr('arduinotrace.trace.TRACE', lambda: None)
    Serial.clear()
    TRACE()  # Should do nothing (no exception, no logs)
    assert Serial.get_output() == []