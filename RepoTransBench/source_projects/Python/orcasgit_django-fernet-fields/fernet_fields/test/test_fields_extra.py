import pytest

from fernet_fields.fields import FernetField

def test_fernetfield_encrypt_decrypt():
    field = FernetField()
    data = b"SensitiveData123"
    encrypted = field.get_prep_value(data)
    decrypted = field.from_db_value(encrypted, None, None, None)
    assert decrypted == data

def test_fernetfield_different_data():
    field = FernetField()
    value = b"AnotherSecret"
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
    b"param_1",
    b"param_2",
    b"param_3",
])
def test_fernetfield_parametrize(val):
    field = FernetField()
    encrypted = field.get_prep_value(val)
    decrypted = field.from_db_value(encrypted, None, None, None)
    assert decrypted == val