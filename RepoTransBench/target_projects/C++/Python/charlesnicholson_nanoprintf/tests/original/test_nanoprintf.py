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

def test_nanoprintf_integer():
    buf = ""
    n, buf = npf_snprintf(buf, 128, "%d", 42)
    assert n == 2
    assert buf == "42"

def test_nanoprintf_string():
    buf = ""
    n, buf = npf_snprintf(buf, 128, "Hello %s", "World")
    assert n == 11
    assert buf == "Hello World"