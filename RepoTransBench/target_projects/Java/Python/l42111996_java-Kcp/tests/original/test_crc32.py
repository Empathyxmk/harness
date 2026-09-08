import zlib

def test_crc32_value():
    data = bytes([0]*1024)
    crc32val = zlib.crc32(data)
    # just check it's an integer and fixed value for 0s 1024 bytes
    assert isinstance(crc32val, int)
    assert crc32val == 3308416167

def test_crc32_update():
    # Update via memory buffer
    data = bytearray([0]*1024)
    crc = zlib.crc32(data)
    assert crc == 3308416167