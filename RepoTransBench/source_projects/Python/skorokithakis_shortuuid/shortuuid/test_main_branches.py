import pytest
import uuid
from shortuuid.main import ShortUUID, int_to_string, string_to_int

def test_int_to_string_zero_and_empty():
    alphabet = list("abcd")
    # For number zero
    assert int_to_string(0, alphabet, padding=5) == "aaaaa"

def test_int_to_string_short_padding():
    alphabet = list("abc")
    assert int_to_string(2, alphabet, padding=1) == "c"

def test_decode_legacy_true_behavior():
    s = ShortUUID()
    u = uuid.uuid4()
    enc = s.encode(u)
    rev = enc[::-1]
    # legacy=True decodes reversed string
    u_dec = s.decode(rev, legacy=True)
    assert isinstance(u_dec, uuid.UUID)

def test_set_alphabet_dont_sort_preserved_order():
    s = ShortUUID(alphabet="ACBXYZ", dont_sort_alphabet=True)
    assert s.get_alphabet() == "ACBXYZ"

def test_set_alphabet_errors():
    s = ShortUUID()
    # Should raise for 1-char alphabet even if dont_sort_alphabet
    with pytest.raises(ValueError):
        s.set_alphabet("z", dont_sort_alphabet=True)
    # Should raise for not string alphabet (fix: must be a string or iterable: here should not error, so we pass non-string but iterable that is not valid)
    with pytest.raises(ValueError):
        s.set_alphabet([], dont_sort_alphabet=True)