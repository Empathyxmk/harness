import pytest
import uuid
from shortuuid import (
    encode,
    decode,
    get_alphabet,
    random as shortuuid_random,
    set_alphabet,
    ShortUUID,
    uuid as shortuuid_uuid,
)

def test_int_to_string_and_string_to_int_identity():
    from shortuuid.main import int_to_string, string_to_int

    alphabet = list("abcdef1234")
    for num in [0, 1, 10, 123456789, 2**64]:
        s = int_to_string(num, alphabet, padding=8)
        restored = string_to_int(s, alphabet)
        assert restored == num

def test_encode_and_decode_roundtrip():
    u = uuid.uuid4()
    s = encode(u)
    u2 = decode(s)
    assert str(u) == str(u2)

def test_get_and_set_alphabet():
    # Set, then get, verify
    alphabet = "zyxwvutsrqponmlkjihgfedcba234567"
    set_alphabet(alphabet)
    assert sorted(get_alphabet()) == sorted(alphabet)

def test_random_length():
    rand1 = shortuuid_random(length=5)
    assert isinstance(rand1, str)
    assert len(rand1) == 5

def test_set_alphabet_invalid(monkeypatch):
    # Patch ShortUUID.set_alphabet to test ValueError
    s = ShortUUID()
    with pytest.raises(ValueError):
        s.set_alphabet("a", dont_sort_alphabet=False)

def test_shortuuid_encode_uuid_type_error():
    short = ShortUUID()
    with pytest.raises(ValueError):
        short.encode("notauuid")

def test_shortuuid_decode_str_type_error():
    short = ShortUUID()
    with pytest.raises(ValueError):
        short.decode(12345)

def test_shortuuid_properties_and_methods():
    s = ShortUUID()
    # Test _length property
    assert isinstance(s._length, int)
    # get_alphabet returns a string
    assert isinstance(s.get_alphabet(), str)

def test_shortuuid_uuid_random_and_named():
    s = ShortUUID()
    anon = s.uuid()
    assert isinstance(anon, str)
    # name as URL
    url_id = s.uuid(name="https://example.com")
    assert isinstance(url_id, str)
    # name as DNS
    dns_id = s.uuid(name="myname")
    assert isinstance(dns_id, str)

def test_shortuuid_random_method():
    s = ShortUUID()
    result = s.random(length=6)
    assert isinstance(result, str)
    assert len(result) == 6

def test_decode_legacy_behavior():
    u = uuid.uuid4()
    s = encode(u)
    # legacy should not raise, string will be reversed before decoding
    u2 = decode(s[::-1], legacy=True)
    assert isinstance(u2, uuid.UUID)

def test_string_to_int_invalid_char():
    from shortuuid.main import string_to_int
    alphabet = list("abc")
    with pytest.raises(ValueError):
        string_to_int("ad", alphabet)

def test_int_to_string_with_padding():
    from shortuuid.main import int_to_string
    alphabet = list("abcde12345")
    s = int_to_string(5, alphabet, padding=8)
    assert len(s) == 8

def test_shortuuid_set_alphabet_dont_sort():
    s = ShortUUID(alphabet="cba", dont_sort_alphabet=True)
    assert s.get_alphabet() == "cba"