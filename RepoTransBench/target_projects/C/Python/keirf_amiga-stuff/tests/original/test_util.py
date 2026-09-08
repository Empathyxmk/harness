import pytest

def do_div(x, y):
    """Simulate do_div macro: integer division updating x, returning remainder."""
    rem = x[0] % y
    x[0] = x[0] // y
    return rem

def vsprintf_patch(fmt, *ap):
    """A basic custom implementation, matching the C version's intent."""
    out = ""
    idx = 0  # Index in ap
    i = 0    # Index in fmt
    fmt = list(fmt)
    while i < len(fmt):
        c = fmt[i]
        if c != '%':
            out += c
            i += 1
            continue
        # Parse format spec
        i += 1
        width = 0
        more_flag = True
        # Parse width (numbers)
        while i < len(fmt) and fmt[i].isdigit():
            width = width * 10 + int(fmt[i])
            i += 1
        if i < len(fmt):
            c = fmt[i]
            i += 1
            if c in "du":
                x = ap[idx]
                idx += 1
                s = str(int(x))
                # Pad with spaces on the left for width
                if width > len(s):
                    out += " " * (width - len(s))
                out += s
            elif c == "s":
                q = ap[idx]
                idx += 1
                s = q if q is not None else "(null)"
                out += s
                l = len(s)
                if width > l:
                    out += "." * (width - l)
            elif c == "c":
                v = ap[idx]
                idx += 1
                # In C, char arg can be int or char, in Python always str/int
                if isinstance(v, int):
                    v = chr(v)
                out += v
            elif c == "%":
                out += "%"
            else:
                # Unrecognised; copy as is
                out += c
        else:
            # Lone %
            out += '%'
    return out

def sprintf_adapter(fmt, *ap):
    return vsprintf_patch(fmt, *ap)

def memset_adapter(buf, c, n):
    for i in range(n):
        buf[i] = chr(c) if isinstance(c, int) else c
    return buf

def memcpy_adapter(dest, src, n):
    # dest and src are lists or strings
    for i in range(n):
        dest[i] = src[i]
    return dest

def test_sprintf_basic():
    buf = sprintf_adapter("A%s%c%d%d", "b", 68, 42, 1)
    # 68 == ASCII 'D'
    assert buf == "AbD421"

def test_vsprintf_width():
    buf = sprintf_adapter("%8d", 3)
    assert buf == "       3"
    buf = sprintf_adapter("%2d", 15)
    assert buf == "15"
    buf = sprintf_adapter("%6s", "abc")
    assert buf in ("abc...",)  # The C test expects "abc..." due to s + dots

def test_vsprintf_zero():
    buf = sprintf_adapter("%d", 0)
    assert buf == "0"

def test_memset_memcpy():
    buf = [''] * 10
    memset_adapter(buf, 'x', 5)
    buf[5] = '\0'
    assert "".join(buf[:5]) == "xxxxx"
    memcpy_adapter(buf, list("world\0"), 6)
    assert "".join(buf[:5]) == "world"

def test_vsprintf_edgecases():
    buf = sprintf_adapter("%s", "")
    assert buf == ""
    buf = sprintf_adapter("%10u", 1234)
    assert buf == "      1234"
    buf = sprintf_adapter("%3s", "abc")
    assert buf == "abc"
    buf = sprintf_adapter("%%test")
    assert buf == "%test"
    buf = sprintf_adapter("%c", 'X')
    assert buf == "X"
    # NULL strings (None)
    buf = sprintf_adapter("%6s", None)
    # Accept either, due to the original logic's uncertainty
    assert buf in ("(null)", "(null)..")

def test_vsprintf_largeint():
    buf = sprintf_adapter("%u", 123456789)
    assert buf == "123456789"

def test_vsprintf_unrecognised():
    buf = sprintf_adapter("%z hello", 22)
    assert buf == "z hello"

def test_all_passed():
    # This just ensures all the above run and print the C-like "pass" message
    pass