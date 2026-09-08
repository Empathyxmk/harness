import pytest
from arduinotrace.trace import SpyingSerial

def test_trace_with_alternative_serial_public():
    alt_public = SpyingSerial()
    alt_public.clear()
    alt_public.write("TRACE: called\n")
    alt_public.write("TRACE: called\n")
    output = alt_public.get_output()
    assert output.count("TRACE: called\n") == 2