import pytest

from src.libhfs_unicode import utf8_to_utf16, utf16_to_utf8, utf8_to_utf16_lenient

def test_utf8_to_utf16_ascii_public():
    src = "Hello, Test!"
    dst = [0]*256
    ulen = utf8_to_utf16(dst, 256, src, len(src), 0, [0])
    assert ulen == len(src)
    for i in range(ulen):
        assert dst[i] == ord(src[i])

def test_utf8_to_utf16_emoji_public():
    src = "Good \U0001F60A luck."  # U+1F60A is the emoji
    dst = [0]*256
    ulen = utf8_to_utf16(dst, 256, src, len(src), 0, [0])
    # "Good " (5), emoji (surrogate pair counted as 2), " luck." (6) => 13 code units
    assert ulen == 13
    # The surrogates for U+1F60A
    assert dst[5] == 0xD83D
    assert dst[6] == 0xDE0A

def test_utf8_to_utf16_invalid2byte_public():
    src = "ABC" + "\xC2" + "Z"   # lone 0xC2
    dst = [0]*256
    err = [0]
    outlen = utf8_to_utf16_lenient(src, dst, 256, err)
    # Should substitute invalid byte, so length is 5, error nonzero
    assert outlen == 5 and err[0] != 0

def test_utf16_to_utf8_cyrillic_public():
    # "Привет!"
    src = [0x041F, 0x0440, 0x0438, 0x0432, 0x0435, 0x0442, 0x21, 0]
    dst = ['']*64
    outlen = utf16_to_utf8(dst, 64, src, len(src), 0, [0])
    # Compare to UTF-8 for "Привет!"
    utf8_str = "\xD0\x9F\xD1\x80\xD0\xB8\xD0\xB2\xD0\xB5\xD1\x82!"
    result = ''.join(dst[:outlen])
    assert result == utf8_str
    assert outlen == len(result)

def test_utf16_to_utf8_surrogate_public():
    # Music G Clef U+1D11E -> D834 DD1E
    src = [0xD834, 0xDD1E, 0]
    dst = ['']*16
    outlen = utf16_to_utf8(dst, 16, src, len(src), 0, [0])
    result = ''.join(dst[:outlen])
    assert result == "\xF0\x9D\x84\x9E"
    assert outlen == 4

def test_utf8_to_utf16_unexpected_continuation_public():
    # Completely invalid UTF-8: 0x80
    src = "XY" + "\x80" + "Z"
    dst = [0]*16
    err = [0]
    outlen = utf8_to_utf16_lenient(src, dst, 16, err)
    assert outlen == 4 and err[0] != 0