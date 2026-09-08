import pytest
from src.keygrip import Keygrip

def test_static_sign_throws():
    with pytest.raises(TypeError):
        Keygrip.sign()

def test_static_verify_throws():
    with pytest.raises(TypeError):
        Keygrip.verify()

def test_static_index_throws():
    with pytest.raises(TypeError):
        Keygrip.index()

def test_keygrip_instantiate_empty_keys():
    keygrip = Keygrip([])
    assert isinstance(keygrip, Keygrip)

def test_keygrip_instantiate_with_strings():
    keygrip = Keygrip(["abc", "def"])
    assert isinstance(keygrip, Keygrip)

def test_keygrip_instantiate_with_utf8_bytes():
    keygrip = Keygrip([b'abc', b'def'])
    assert isinstance(keygrip, Keygrip)

def test_keygrip_instantiate_with_bytes_and_strings():
    keygrip = Keygrip([b'abc', "def"])
    assert isinstance(keygrip, Keygrip)

def test_keygrip_instantiate_with_invalid_key_type():
    with pytest.raises(TypeError):
        Keygrip([123, "abc"])

def test_sign_and_verify_work():
    keys = ["abc"]
    kg = Keygrip(keys)
    data = "valuedata"
    digest = kg.sign(data)
    assert kg.verify(data, digest)
    assert kg.index(data, digest) == 0

def test_different_key_order_changes_index():
    keys = ["abc", "def"]
    kg = Keygrip(keys)
    kg2 = Keygrip(keys[::-1])
    data = "foo"
    digest = kg.sign(data)
    idx1 = kg.index(data, digest)
    idx2 = kg2.index(data, digest)
    assert idx1 == 0
    assert idx2 == 1

def test_sign_with_bytes_data_is_valid():
    keys = ["abc"]
    kg = Keygrip(keys)
    data = b"bin"
    digest = kg.sign(data)
    assert kg.verify(data, digest)
    assert kg.index(data, digest) == 0

def test_sign_with_non_string_bytes_keys():
    # This is valid because we convert bytes to str in __init__
    keys = [b"abc"]
    kg = Keygrip(keys)
    data = "data"
    digest = kg.sign(data)
    assert kg.verify(data, digest)

def test_sign_with_invalid_data_type():
    keys = ["abc"]
    kg = Keygrip(keys)
    with pytest.raises(TypeError):
        kg.sign(123)

def test_verify_with_invalid_digest_type():
    keys = ["abc"]
    kg = Keygrip(keys)
    with pytest.raises(TypeError):
        kg.verify("data", 456)