import pytest

def is_valid_png(data):
    PNG_SIG = b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A'
    if len(data) < 8:
        return False
    return data[:8] == PNG_SIG

def test_parse_different_png_header():
    png_header = [0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A]
    png_chunk = [
        0x00, 0x00, 0x00, 0x0D,
        0x49, 0x48, 0x44, 0x52,
        0x00, 0x00, 0x01, 0x00,
        0x00, 0x00, 0x01, 0x00,
        0x08, 0x06, 0x00, 0x00, 0x00,
        0x5C, 0x72, 0xA8, 0x66
    ]
    png_data = bytearray(png_header + png_chunk)
    assert is_valid_png(png_data)

def test_reject_non_png_data():
    fake = bytearray([1,2,3,4,5,6,7,8])
    assert not is_valid_png(fake)