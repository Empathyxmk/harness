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
                if isinstance(v, int):
                    v = chr(v)
                out += v
            elif c == "%":
                out += "%"
            else:
                out += c
        else:
            out += '%'
    return out

def sprintf_adapter(fmt, *ap):
    return vsprintf_patch(fmt, *ap)

def memset_adapter(buf, c, n):
    for i in range(n):
        buf[i] = chr(c) if isinstance(c, int) else c
    return buf

def memcpy_adapter(dest, src, n):
    for i in range(n):
        dest[i] = src[i]
    return dest

def test_sprintf_basic_public():
    buf = sprintf_adapter("%c%s%d%d", 'Z', "oo", 123, 0)
    assert buf == "Zoo1230"
    buf = sprintf_adapter("HELLO")
    assert buf == "HELLO"

def test_vsprintf_width_public():
    buf = sprintf_adapter("%4d", 17)
    assert buf == "  17"
    buf = sprintf_adapter("%7d", 31)
    assert buf == "     31"
    buf = sprintf_adapter("%5s", "xyz")
    assert buf == "xyz.."

def test_vsprintf_zero_public():
    buf = sprintf_adapter("%d", 0)
    assert buf == "0"

def test_memset_memcpy_public():
    buf = [''] * 10
    memset_adapter(buf, '*', 4)
    buf[4] = '\0'
    assert "".join(buf[:4]) == "****"
    memcpy_adapter(buf, list("data\0"), 5)
    assert "".join(buf[:4]) == "data"

def test_vsprintf_edgecases_public():
    buf = sprintf_adapter("%s", "PUBLIC")
    assert buf == "PUBLIC"
    buf = sprintf_adapter("%8u", 4321)
    assert buf == "    4321"
    buf = sprintf_adapter("%4s", "x")
    assert buf == "x..."
    buf = sprintf_adapter("%%%%")
    assert buf == "%%"
    buf = sprintf_adapter("%c", 'P')
    assert buf == "P"
    buf = sprintf_adapter("%7s", None)
    assert buf in ("(null)", "(null)..")

def test_all_util_public():
    pass