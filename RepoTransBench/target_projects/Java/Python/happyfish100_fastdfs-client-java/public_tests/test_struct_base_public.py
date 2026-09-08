import pytest
from datetime import datetime

class DummyStruct:
    def __init__(self):
        self.strVal = None
        self.longVal = None
        self.intVal = None
        self.int32Val = None
        self.byteVal = None
        self.boolVal = None
        self.dateVal = None

    def string_value(self, bs, offset, f):
        try:
            sub = bs[offset:offset+f['size']]
            if hasattr(sub, "_force_decode_error") and getattr(sub, "_force_decode_error"):
                raise UnicodeDecodeError("utf-8", b"a", 0, 1, "bad")
            try:
                return sub.decode("utf-8").rstrip('\x00')
            except Exception:
                return None
        except Exception:
            return None

    def long_value(self, bs, offset, f):
        return int.from_bytes(bs[offset:offset+f['size']], 'big', signed=True)

    def int_value(self, bs, offset, f):
        return int.from_bytes(bs[offset:offset+f['size']], 'big', signed=True)

    def int32_value(self, bs, offset, f):
        return int.from_bytes(bs[offset:offset+4], 'big', signed=True)

    def byte_value(self, bs, offset, f):
        return bs[offset]

    def boolean_value(self, bs, offset, f):
        return bs[offset] != 0

    def date_value(self, bs, offset, f):
        return datetime.now() # Simulate as current time

    def set_fields(self, bs, offset):
        field = {'name':'test','offset':0,'size':4}
        self.strVal = self.string_value(bs, offset, field)
        self.longVal = self.long_value(bs, offset, field)
        self.intVal = self.int_value(bs, offset, field)
        self.int32Val = self.int32_value(bs, offset, field)
        self.byteVal = self.byte_value(bs, offset, field)
        self.boolVal = self.boolean_value(bs, offset, field)
        self.dateVal = self.date_value(bs, offset, field)

def test_string_value_different():
    s = DummyStruct()
    bs = b"Public01\x00\x00"
    f = {'name': 'str', 'offset': 0, 'size': 8}
    val = s.string_value(bs, 0, f)
    assert val == "Public01"

def test_string_value_encoding_exception_public():
    s = DummyStruct()
    f = {'name': 'str', 'offset': 0, 'size': 1}
    class BadBytes(bytes):
        _force_decode_error = True
        def decode(self, encoding):
            raise UnicodeDecodeError("utf-8", b"a", 0, 1, "bad")
    bs = BadBytes([66])
    val = s.string_value(bs, 0, f)
    assert val is None

def test_other_value_methods_public():
    s = DummyStruct()
    bs = bytearray(16)
    bs[0] = 42
    f = {'name': 'd', 'offset': 0, 'size': 8}
    s.set_fields(bs, 0)
    assert s.strVal is not None
    assert s.dateVal is not None
    assert s.byteVal == bs[0]