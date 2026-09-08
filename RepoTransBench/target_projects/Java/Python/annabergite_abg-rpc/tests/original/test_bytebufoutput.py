import pytest

class ByteBuf:
    def __init__(self, cap):
        self._data = bytearray()
        self._released = False

    def readableBytes(self):
        return len(self._data)

    def write(self, b):
        self._data.append(b)

class ByteBufOutput:
    def __init__(self, buf):
        self.byteBuf = buf
        self._max_capacity = None

    def setBuffer(self, buf, max_capacity=None):
        if max_capacity is not None and max_capacity < -1:
            raise ValueError("Illegal buffer capacity")
        self.byteBuf = buf
        self._max_capacity = max_capacity

    def write(self, b):
        self.byteBuf.write(b)

    def release(self):
        self.byteBuf = None

def test_constructor_set_buffer():
    buf = ByteBuf(8)
    out = ByteBufOutput(buf)
    assert out is not None
    out.setBuffer(None)  # should not throw

def test_set_buffer_with_capacity():
    buf = ByteBuf(8)
    out = ByteBufOutput(buf)
    out.setBuffer(buf, -1)
    with pytest.raises(ValueError):
        out.setBuffer(buf, -2)

def test_write_and_release():
    buf = ByteBuf(4)
    out = ByteBufOutput(buf)
    out.write(65)
    assert buf.readableBytes() == 1
    out.release()
    assert out.byteBuf is None