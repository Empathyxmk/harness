import pytest

# Placeholder for implementation import:
# from cnetpp.base import StringUtils, StringPiece

class StringUtils:
    @staticmethod
    def SplitByChars(s, chars):
        if isinstance(s, StringPiece):
            s = s.s
        return [part for part in s.split(chars) if part]

    @staticmethod
    def ToVarint32(i, buf):
        value = i
        bytes_written = 0
        while value > 0x7F:
            buf[bytes_written] = value & 0x7F | 0x80
            value >>= 7
            bytes_written += 1
        buf[bytes_written] = value & 0x7F
        bytes_written += 1
        return bytes_written

    @staticmethod
    def ParseVarint32(sp, out):
        res = 0
        shift = 0
        for b in sp.s:
            b = b if isinstance(b, int) else ord(b)
            res |= (b & 0x7F) << shift
            if not (b & 0x80):
                out[0] = res
                return True
            shift += 7
            if shift > 35:
                return False
        return False

    @staticmethod
    def PutUint32(i, buf):
        import struct
        buf[:4] = struct.pack("<I", i)

    @staticmethod
    def ToUint32(sp):
        import struct
        return struct.unpack("<I", bytes(sp.s[:4]))[0]

class StringPiece:
    def __init__(self, s, length=None):
        if isinstance(s, bytes):
            self.s = s[:length] if length else s
        else:
            self.s = s[:length] if length else s
    def set(self, s, length=None):
        if isinstance(s, bytes):
            self.s = s[:length] if length else s
        else:
            self.s = s[:length] if length else s
    def __str__(self):
        return self.s

def test_SplitByCharsTest01():
    str_val = "abc defhi gk"
    res = StringUtils.SplitByChars(StringPiece(str_val[:7]), " ")
    assert len(res) == 2
    res = StringUtils.SplitByChars(str_val, " ")
    assert len(res) == 3

def test_Varint32Test():
    # C++ test loops to 0x7fffffff, that's 2**31-1, which is too slow/costly for Python test.
    # Instead, let's check representative values.
    test_values = [0, 1, 127, 128, 255, 16384, 2**31-1]
    for i in test_values:
        buf = bytearray(10)
        length = StringUtils.ToVarint32(i, buf)
        j = [0]
        sp = StringPiece(buf[:length])
        assert StringUtils.ParseVarint32(sp, j)
        assert j[0] == i

def test_Uint32Test():
    import struct
    # C++ test loops to 0xffffffff, that's 2**32-1, too large for full Python test.
    # We'll sample edge/representative values.
    test_values = [0, 1, 2, 255, 256, 1024, 65535, 2**31-1, 2**32-1]
    for i in test_values:
        buf = bytearray(10)
        StringUtils.PutUint32(i, buf)
        sp = StringPiece(buf, 4)
        j = StringUtils.ToUint32(sp)
        assert j == i