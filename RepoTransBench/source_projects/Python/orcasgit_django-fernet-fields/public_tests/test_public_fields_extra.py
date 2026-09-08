import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fernet_fields.fields import FernetField
import pytest

def test_fernetfield_encrypt_decrypt():
    field = FernetField()
    data = b"SensitivePublicData123"
    encrypted = field.get_prep_value(data)
    decrypted = field.from_db_value(encrypted, None, None, None)
    assert decrypted == data

def test_fernetfield_different_data():
    field = FernetField()
    value = b"UniqueBytesForPublicTest"
    encrypted = field.get_prep_value(value)
    decrypted = field.from_db_value(encrypted, None, None, None)
    assert decrypted == value

def test_fernetfield_handles_empty_bytes():
    field = FernetField()
    value = b""
    encrypted = field.get_prep_value(value)
    decrypted = field.from_db_value(encrypted, None, None, None)
    assert decrypted == b""

@pytest.mark.parametrize("val", [
    b"public_param_1",
    b"another_param_public_2",
    b"extra_data_public_3",
])
def test_fernetfield_parametrize(val):
    field = FernetField()
    encrypted = field.get_prep_value(val)
    decrypted = field.from_db_value(encrypted, None, None, None)
    assert decrypted == val