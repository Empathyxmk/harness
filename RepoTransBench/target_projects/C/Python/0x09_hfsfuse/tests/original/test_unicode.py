import pytest
import string

from src.libhfs_unicode import utf8_to_utf16, utf16_to_utf8

def str2u16(s):
    return [ord(c) for c in s]

def u16list_to_str(u16, length=None):
    # Convert a list of uint16 ints to a unicode string.
    n = length if length is not None else len(u16)
    return ''.join(chr(x) for x in u16[:n] if x != 0)

def bytestr_from_charlist(lst):
    return ''.join(lst).replace('\x00', '')

def test_ascii_to_utf16_roundtrip():
    ascii = "hello"
    utf16 = [0]*10
    utf8 = ['']*10
    err = [0]
    u16len = utf8_to_utf16(utf16, 10, ascii, len(ascii), 0, err)
    assert err[0] == 0
    assert u16len == len(ascii)
    u8len = utf16_to_utf8(utf8, 10, utf16, u16len, 0, err)
    assert err[0] == 0
    # Reconstruct string from utf8 char list
    s = ''.join(utf8[:u8len])
    assert u8len == len(ascii)
    assert ascii == s

def test_utf8_to_utf16_invalid():
    invalid = "\xF5"
    utf16 = [0]*2
    err = [0]
    outlen = utf8_to_utf16(utf16, 2, invalid, 1, 1, err)
    assert outlen == 1 and err[0] != 0

def test_utf8_to_utf16_overlong():
    # Overlong 0xC0 0xAF sequence
    overlong = bytes([0xC0, 0xAF]).decode('latin1')
    utf16 = [0]*2
    err = [0]
    outlen = utf8_to_utf16(utf16, 2, overlong, 2, 1, err)
    assert outlen == 1 and err[0] != 0

def test_utf16_to_utf8_surrogate():
    sur = [0xD800, 0]  # high surrogate alone
    utf8 = ['']*10
    err = [0]
    outlen = utf16_to_utf8(utf8, 10, sur, 1, 1, err)
    assert outlen == 0 and err[0] != 0

def test_utf8_nullptrs():
    # All null - should report error
    err = [None]
    r = utf8_to_utf16(None, 0, None, 0, 0, err)
    assert r == 0
    assert err[0] != 0

def test_utf16_nullptrs():
    err = [None]
    r = utf16_to_utf8(None, 0, None, 0, 0, err)
    assert r == 0
    assert err[0] != 0

def test_utf8_zerolen():
    utf16 = [0]
    err = [-1]
    out = utf8_to_utf16(utf16, 1, "", 0, 0, err)
    assert out == 0
    assert err[0] == 0

def test_utf16_zerolen():
    out = ['\x00']
    err = [-1]
    r = utf16_to_utf8(out, 1, [0], 0, 0, err)
    assert r == 0
    assert err[0] == 0

def test_utf8_to_utf16_dstlen_zero():
    ascii = "a"
    err = [0]
    # "fake" pointer in C, just test dstlen=0 logic in Python
    r = utf8_to_utf16([0], 0, ascii, 1, 0, err)
    assert r == 0
    # Should set err nonzero
    assert err[0] == 1

def test_utf16_to_utf8_dstlen_zero():
    in16 = [10, 0]
    err = [0]
    r = utf16_to_utf8([''], 0, in16, 1, 0, err)
    assert r == 0
    assert err[0] == 1

def test_utf8_to_utf16_short_dst():
    ascii = "abcdef"
    utf16 = [0]*2
    err = [42]
    out = utf8_to_utf16(utf16, 2, ascii, len(ascii), 0, err)
    assert err[0] == 0
    assert out == 2

def test_utf16_to_utf8_short_dst():
    utf16 = [ord(c) for c in "abcde"]
    out = ['']*2
    err = [42]
    outlen = utf16_to_utf8(out, 2, utf16, 5, 0, err)
    assert err[0] == 0
    assert outlen == 2