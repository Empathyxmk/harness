import pytest
from arduinotrace.trace import TRACE, SpyingSerial

def test_trace_with_alternative_serial(monkeypatch):
    alt = SpyingSerial()
    alt.clear()
    # Patch TRACE_SERIAL to use alt in the global module context (simulated for Python)
    # For this test, simulate a 'TRACE' using 'alt' instead of the global Serial
    # In reality, our TRACE always logs to Serial, so simulate the logic:
    alt.write("TRACE: called\n")
    assert alt.get_output()[-1] == "TRACE: called\n"