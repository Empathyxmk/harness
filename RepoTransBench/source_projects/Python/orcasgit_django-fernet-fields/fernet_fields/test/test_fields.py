from django.utils.encoding import force_bytes
try:
    from django.utils.encoding import force_text
except ImportError:
    from django.utils.encoding import force_str as force_text

import pytest

from fernet_fields.fields import EncryptedTextField, EncryptedCharField

def test_encrypted_field():
    value = "Secret Data"
    field = EncryptedTextField()
    enc = field.get_prep_value(value)
    dec = field.from_db_value(enc, None, None, None)
    assert dec == value

def test_encrypted_char_field():
    value = "HelloWorld"
    field = EncryptedCharField(max_length=32)
    enc = field.get_prep_value(value)
    dec = field.from_db_value(enc, None, None, None)
    assert dec == value

def test_encrypted_field_empty_string():
    value = ""
    field = EncryptedTextField()
    enc = field.get_prep_value(value)
    dec = field.from_db_value(enc, None, None, None)
    assert dec == ""

@pytest.mark.parametrize("val", [
    "the quick brown fox",
    "test_string_value",
    "another test message",
])
def test_encrypted_field_parametrize(val):
    field = EncryptedTextField()
    enc = field.get_prep_value(val)
    dec = field.from_db_value(enc, None, None, None)
    assert dec == val