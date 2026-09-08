import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fernet_fields.fields import FernetField, EncryptedTextField, EncryptedCharField
import pytest

def test_encrypted_field_basic():
    value = "This is secret data for pub"
    field = EncryptedTextField()
    enc = field.get_prep_value(value)
    dec = field.from_db_value(enc, None, None, None)
    assert dec == value

def test_encrypted_char_field():
    value = "AlphaBravo"
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
    "fox jumps over the lazy dog",
    "crazy_test_value_PUBLIC_CASE",
    "another secret message",
])
def test_encrypted_field_parametrize(val):
    field = EncryptedTextField()
    enc = field.get_prep_value(val)
    dec = field.from_db_value(enc, None, None, None)
    assert dec == val