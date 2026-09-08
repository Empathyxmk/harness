import pytest

import src.edbase32 as base32

def test_encode_hello_world():
    input_bytes = b'Hello World'
    result = base32.encode(input_bytes)
    assert result == 'JBSWY3DPEBLW64TMMQ======'

def test_encode_null_undefined():
    assert base32.encode(None) is None

def test_encode_short_inputs():
    assert base32.encode(b'M') == 'JU======'
    assert base32.encode(b'Ma') == 'JVQQ===='
    assert base32.encode(b'Man') == 'JVQW4==='
    assert base32.encode(b'Man1') == 'JVQW4MI='

def test_encode_empty_buffer():
    assert base32.encode(b'') == ''