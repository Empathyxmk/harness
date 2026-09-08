import pytest

def is_ascii(s):
    try:
        s.encode("ascii")
        return True
    except Exception:
        return False

def utf8_bytes(s):
    return s.encode("utf-8")

def latin1_bytes(s):
    return s.encode("latin-1", "ignore")

class UnsafeStringUtils:
    @staticmethod
    def getUTF8Bytes(s):
        return utf8_bytes(s)
    @staticmethod
    def getLatin1Bytes(s):
        return latin1_bytes(s)

class UnsafeUtils:
    @staticmethod
    def unsafe():
        # Simulate allocation of new string (not meaningful in Python)
        class Unsafe:
            def allocateInstance(self, cls):
                return cls()
        return Unsafe()

def test_get_bytes_methods():
    s = "https://github.com/twitter/finagle/blob/master/finagle-netty4/src/main/scala/com/twitter/finagle/netty4/Netty4Listener.scala"

    # Normal utf-8
    b1 = s.encode("utf-8")
    assert b1 == utf8_bytes(s)

    # is_ascii
    ascii = is_ascii(s)
    if ascii:
        b2 = s.encode("ascii")
        assert b2 == latin1_bytes(s)
    else:
        b2 = utf8_bytes(s)
        assert b2 == utf8_bytes(s)

    # with buffer (simulate)
    ascii = is_ascii(s)
    if ascii:
        bbuf = bytearray(len(s))
        b_plain = s.encode("ascii")
        assert bytes(bbuf[:len(b_plain)]) == b_plain[:len(bbuf)]
    else:
        bbuf = utf8_bytes(s)
        assert bbuf == utf8_bytes(s)

    # UnsafeStringUtils
    assert UnsafeStringUtils.getUTF8Bytes(s) == utf8_bytes(s)
    # latin-1 (may lose data)
    assert UnsafeStringUtils.getLatin1Bytes(s) == latin1_bytes(s)

def test_string_instance_by_new():
    s = str()
    assert isinstance(s, str)

def test_string_instance_by_unsafe():
    s = UnsafeUtils.unsafe().allocateInstance(str)
    assert isinstance(s, str)