import pytest
from src.blueimp_md5 import md5

def test_create_hex_md5_ascii():
    assert md5('value') == '2063c1608d6e0baf80249c42e2be5804'

def test_create_hex_md5_utf8():
    assert md5('日本') == '4dbed2e657457884e67137d3514119b3'

def test_create_hmac_hex_md5_ascii():
    assert md5('value', 'key') == '01433efd5f16327ea4b31144572c67f6'

def test_create_hmac_hex_md5_utf8():
    assert md5('日本', '日本') == 'c78b8c7357926981cc04740bd3e9d015'

def test_create_raw_md5_ascii():
    result = md5('value', None, True)
    assert isinstance(result, bytes)
    # Match JavaScript raw: test value for direct string
    expected = b' c\xc1`\x8dn\x0b\xaf\x80$\x9cB\xe2\xbeX\x04'
    assert result == expected

def test_create_raw_md5_utf8():
    result = md5('日本', None, True)
    expected = b'M\xbe\xd2\xe6WEx\x84\xe6q7\xd3QA\x19\xb3'
    assert result == expected

def test_create_hmac_raw_md5_ascii():
    result = md5('value', 'key', True)
    expected = b'\x01C>\xfd_\x162~\xa4\xb3\x11DW,g\xf6'
    assert result == expected

def test_create_hmac_raw_md5_utf8():
    result = md5('日本', '日本', True)
    expected = b'\xc7\x8b\x8csW\x92i\x81\xcc\x04t\x0b\xd3\xe9\xd0\x15'
    assert result == expected