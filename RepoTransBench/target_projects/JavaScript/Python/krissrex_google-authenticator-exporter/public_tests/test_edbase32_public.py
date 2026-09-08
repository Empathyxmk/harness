import pytest

import src.edbase32 as base32

def test_encode_public_string():
    input_bytes = b'OpenAI Rocks!'
    result = base32.encode(input_bytes)
    assert result == 'JBSWY4DMMFZWK3TPOQQGSZJANVZA===='

def test_encode_null_undefined_public():
    assert base32.encode(None) is None

def test_encode_other_short_input():
    assert base32.encode(b'J') == 'JR======'
    assert base32.encode(b'JS') == 'JRSA===='
    assert base32.encode(b'JSt') == 'JRSA2Y=='
    assert base32.encode(b'JSt1') == 'JRSA2ZDG'

def test_encode_empty_buffer_public():
    assert base32.encode(b'') == ''