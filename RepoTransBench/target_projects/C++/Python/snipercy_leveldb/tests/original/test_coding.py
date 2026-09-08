def test_coding_fixed32():
    import struct
    s = b''
    for v in range(1000):
        s += struct.pack('<I', v)
    p = 0
    for v in range(1000):
        actual = struct.unpack('<I', s[p:p+4])[0]
        assert v == actual
        p += 4

def test_coding_fixed64():
    import struct
    for power in range(0,10):
        v = (1 << power)
        part1 = struct.pack('<Q', v - 1)
        part2 = struct.pack('<Q', v + 0)
        part3 = struct.pack('<Q', v + 1)
        assert struct.unpack('<Q', part1)[0] == (v - 1)
        assert struct.unpack('<Q', part2)[0] == v + 0
        assert struct.unpack('<Q', part3)[0] == v + 1

def test_coding_encoding_output():
    import struct
    dst = struct.pack('<I', 0x04030201)
    assert len(dst) == 4
    assert dst[0] == 0x01
    assert dst[1] == 0x02
    assert dst[2] == 0x03
    assert dst[3] == 0x04
    dst64 = struct.pack('<Q', 0x0807060504030201)
    assert len(dst64) == 8
    assert dst64[0] == 0x01
    assert dst64[7] == 0x08

def test_coding_varint32():
    # Python doesn't have builtin varint, mimic with struct.
    def put_varint32(v):
        b = bytearray()
        while v >= 0x80:
            b.append((v & 0x7F) | 0x80)
            v >>= 7
        b.append(v)
        return bytes(b)
    s = b''.join(put_varint32(i) for i in range(50))
    vals = []
    i = 0
    while i < len(s):
        x, shift = 0, 0
        for j in range(5):
            byte = s[i]
            i += 1
            x |= (byte & 0x7F) << (7 * j)
            if (byte & 0x80) == 0:
                break
        vals.append(x)
    assert vals == list(range(50))

def test_coding_varint64():
    def put_varint64(v):
        b = bytearray()
        while v >= 0x80:
            b.append((v & 0x7F) | 0x80)
            v >>= 7
        b.append(v)
        return bytes(b)
    s = b''.join(put_varint64(i) for i in range(50))
    vals = []
    i = 0
    while i < len(s):
        x, shift = 0, 0
        for j in range(10):
            byte = s[i]
            i += 1
            x |= (byte & 0x7F) << (7 * j)
            if (byte & 0x80) == 0:
                break
        vals.append(x)
    assert vals == list(range(50))