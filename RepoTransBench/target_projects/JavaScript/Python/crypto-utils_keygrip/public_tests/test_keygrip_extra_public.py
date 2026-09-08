import pytest
from src.keygrip import Keygrip

def test_static_sign_throws_public():
    with pytest.raises(TypeError):
        Keygrip.sign("public")

def test_static_verify_throws_public():
    with pytest.raises(TypeError):
        Keygrip.verify("value")

def test_static_index_throws_public():
    with pytest.raises(TypeError):
        Keygrip.index(123)

def test_keygrip_empty_keys_passes_public():
    kg = Keygrip([])
    assert isinstance(kg, Keygrip)

def test_keygrip_good_keys_passes_public():
    kg = Keygrip(["abc", "def"])
    assert isinstance(kg, Keygrip)

def test_keygrip_encode_and_sign_public():
    kg = Keygrip(["a"])
    data = "foo"
    digest = kg.sign(data)
    assert kg.verify(data, digest)
    assert kg.index(data, digest) == 0

def test_sign_rejects_non_string_or_bytes_public():
    kg = Keygrip(["a"])
    with pytest.raises(TypeError):
        kg.sign(123)

def test_verify_invalid_digest_type_public():
    kg = Keygrip(["a"])
    with pytest.raises(TypeError):
        kg.verify("test", 456)