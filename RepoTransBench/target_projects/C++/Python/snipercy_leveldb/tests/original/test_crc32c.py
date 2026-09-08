def test_crc32c_standard_results():
    import binascii
    buf = b'\x00'*32
    assert binascii.crc32(buf) & 0xffffffff == 0x8a9136aa
    buf = b'\xff'*32
    assert binascii.crc32(buf) & 0xffffffff == 0x62a8ab43
    buf = bytes([i for i in range(32)])
    assert binascii.crc32(buf) & 0xffffffff == 0x46dd794e
    buf = bytes([31-i for i in range(32)])
    assert binascii.crc32(buf) & 0xffffffff == 0x113fdb5c
    data = bytes([
        0x01, 0xc0, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00,
        0x14, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x04, 0x00,
        0x00, 0x00, 0x00, 0x14,
        0x00, 0x00, 0x00, 0x18,
        0x28, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00,
        0x02, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00,
    ])
    assert binascii.crc32(data) & 0xffffffff == 0xd9963a56

def test_crc32c_values():
    import binascii
    assert binascii.crc32(b"a") != binascii.crc32(b"foo")

def test_crc32c_extend():
    import binascii
    crc1 = binascii.crc32(b"hello ")
    crc2 = binascii.crc32(b"world", crc1)
    assert crc2 == binascii.crc32(b"hello world")

def test_crc32c_mask():
    import binascii
    crc = binascii.crc32(b"foo") & 0xffffffff
    mask1 = (crc >> 15 | crc << 17) + 0xa282ead8 & 0xffffffff
    mask2 = (mask1 >> 15 | mask1 << 17) + 0xa282ead8 & 0xffffffff
    def unmask(m):
        m = (m - 0xa282ead8) & 0xffffffff
        return ((m << 15) | (m >> 17)) & 0xffffffff
    assert mask1 != crc
    assert mask2 != crc
    assert unmask(mask1) == crc
    assert unmask(unmask(mask2)) == crc