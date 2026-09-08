import pytest

def npf_snprintf(buffer, bufsize, fmt, *args):
    """
    Simulate 'nanoprintf' minimal snprintf functionality for demonstration.
    Implement minimal C-like %d, %s, %x used in tests.
    """
    # Very minimal format processor for test demonstration.
    # Only handles "%d", "%s", and "%x" single occurrence.
    # Not general purpose!
    import re
    # First handle cases where both %s and %d etc appear.
    if '%d' in fmt:
        idx = fmt.index('%d')
        before = fmt[:idx]
        after = fmt[idx+2:]
        result = before + str(int(args[0])) + after
        n = len(result)
        if bufsize:
            buffer = result[:bufsize-1]  # C truncates to N-1 and NUL terminates
        else:
            buffer = ''
        return n, buffer
    elif '%x' in fmt:
        idx = fmt.index('%x')
        before = fmt[:idx]
        after = fmt[idx+2:]
        value = int(args[0])
        result = before + hex(value)[2:] + after
        n = len(result)
        if bufsize:
            buffer = result[:bufsize-1]
        else:
            buffer = ''
        return n, buffer
    elif '%s' in fmt:
        idx = fmt.index('%s')
        before = fmt[:idx]
        after = fmt[idx+2:]
        s = str(args[0])
        result = before + s + after
        n = len(result)
        if bufsize:
            buffer = result[:bufsize-1]
        else:
            buffer = ''
        return n, buffer
    else:
        # No formatting
        result = fmt
        n = len(result)
        buffer = result[:bufsize-1]
        return n, buffer

def test_main_public_testcpp():
    # From main_public_test.cpp
    bufA = ""
    rA, bufA = npf_snprintf("", 100, "Num: %d", 777)
    assert rA == 8
    assert bufA == "Num: 777"

    bufB = ""
    rB, bufB = npf_snprintf("", 100, "Word: %s", "Giraffe")
    assert rB == 12
    assert bufB == "Word: Giraffe"

    bufC = ""
    rC, bufC = npf_snprintf("", 100, "Hex: %x", 0xBEEF)
    assert rC == 9
    assert bufC == "Hex: beef"

def test_main_public_testcc():
    # From main_public_test.cc
    buf = ""
    n, buf = npf_snprintf("", 100, "Public: %d", 101)
    assert n == 11
    assert buf == "Public: 101"

    buf2 = ""
    n2, buf2 = npf_snprintf("", 100, "Data: %s", "Zebra")
    assert n2 == 10
    assert buf2 == "Data: Zebra"

    buf3 = ""
    n3, buf3 = npf_snprintf("", 100, "Hex: %x", 0xDEAD)
    assert n3 == 9
    assert buf3 == "Hex: dead"