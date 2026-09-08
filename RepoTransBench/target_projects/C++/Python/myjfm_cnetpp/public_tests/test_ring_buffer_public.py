import pytest

class RingBuffer:
    def __init__(self, capacity):
        self._buf = bytearray(capacity)
        self._cap = capacity
        self._write_pos = 0
        self._read_pos = 0
        self._size = 0

    def Write(self, data, sz):
        if self._cap - self._size < sz:
            return False
        for i in range(sz):
            self._buf[(self._write_pos + i) % self._cap] = data[i] if isinstance(data, bytes) else ord(data[i])
        self._write_pos = (self._write_pos + sz) % self._cap
        self._size += sz
        return True

    def Read(self, out, sz):
        if self._size < sz:
            return 0
        for i in range(sz):
            out[i] = self._buf[(self._read_pos + i) % self._cap]
        self._read_pos = (self._read_pos + sz) % self._cap
        self._size -= sz
        return sz

    def Resize(self, new_cap):
        if new_cap < self._size:
            return False
        old = self._buf
        self._buf = bytearray(new_cap)
        for i in range(self._size):
            self._buf[i] = old[(self._read_pos + i) % self._cap]
        self._cap = new_cap
        self._read_pos = 0
        self._write_pos = self._size
        return True

def test_write_read_and_resize():
    buf = RingBuffer(16)
    data = b"publicdata"
    sz = len(data)
    assert buf.Write(data, sz)
    read = bytearray(16)
    assert buf.Read(read, sz) == sz
    assert bytes(read[:sz]) == b"publicdata"

    assert buf.Resize(32)
    data2 = b"morebuffer"
    sz2 = len(data2)
    assert buf.Write(data2, sz2)
    read2 = bytearray(16)
    assert buf.Read(read2, sz2) == sz2
    assert bytes(read2[:sz2]) == b"morebuffer"