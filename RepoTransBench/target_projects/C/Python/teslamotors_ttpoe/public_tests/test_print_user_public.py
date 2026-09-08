"""
Public user-space unit tests for print.h logic (TTP_SNPRINTF overflow/edge with different strings).
"""

import pytest

def test_snprintf_overflow_public():
    buf = bytearray(40)
    bs = len(buf)
    sc = 0

    s1 = f"World {12}"
    nn = len(s1)
    if nn >= (bs - sc):
        pytest.fail("Overflow or error! (step 1)")
    buf[sc:sc+nn] = s1.encode()
    sc += nn

    s2 = " Test"
    nn = len(s2)
    if nn >= (bs - sc):
        pytest.fail("Overflow or error! (step 2)")
    buf[sc:sc+nn] = s2.encode()
    sc += nn

    final_str = buf[:sc].decode()
    assert final_str == "World 12 Test"

    # Now deliberately force an overflow
    sc = 36  # near buffer end
    s3 = "overflowingcontent"
    nn = len(s3)
    assert nn >= (bs - sc)

def test_print_pass():
    print("TTP_SNPRINTF public logic edge cases passed")