import pytest
from pyzbar import pyzbar_error

def test_pyzbar_error_is_exception():
    assert issubclass(pyzbar_error.PyZbarError, Exception)

def test_pyzbar_error_raise_and_str():
    e = pyzbar_error.PyZbarError("fail")
    with pytest.raises(pyzbar_error.PyZbarError):
        raise e
    assert str(e) == "fail"