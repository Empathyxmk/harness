# public_tests/test_spdy_rst_stream_public.py
import pytest

def fake_rst_stream_error(code: int) -> int:
    """
    Simulates a function returning different error/status codes.
    Corresponds to tests/test_spdy_rst_stream_public.c.
    """
    if code == 6:
        return -106
    if code == 17:
        return -117
    return 1

def test_spdy_rst_stream_public_error_codes():
    """
    Tests the fake_rst_stream_error function with specific inputs.
    """
    assert fake_rst_stream_error(6) == -106
    assert fake_rst_stream_error(17) == -117
    assert fake_rst_stream_error(88) == 1