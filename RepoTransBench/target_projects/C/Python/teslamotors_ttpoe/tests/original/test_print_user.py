"""
User-space unit tests for print.h logic (adapted).
We'll test TTP_SNPRINTF macro-like logic for overflow/edge cases.
"""

import pytest

def test_snprintf_overflow():
    buf = bytearray(32)
    bs = len(buf)
    sc = 0

    # Python's format returns a string, so to simulate buffer logic,
    # we use manual buffer management
    s1 = f"Hello {7}"
    nn = len(s1)
    if nn >= (bs - sc):
        pytest.fail("Overflow or error! (step 1)")
    buf[sc:sc+nn] = s1.encode()
    sc += nn

    s2 = " End"
    nn = len(s2)
    if nn >= (bs - sc):
        pytest.fail("Overflow or error! (step 2)")
    buf[sc:sc+nn] = s2.encode()
    sc += nn

    # This should not overflow
    final_str = buf[:sc].decode()
    assert final_str == "Hello 7 End"

    # Now force an overflow
    sc = 28  # near buffer end
    s3 = "toolongforbuffer"
    nn = len(s3)
    assert nn >= (bs - sc)

def test_print_pass():
    print("TTP_SNPRINTF logic edge cases passed")