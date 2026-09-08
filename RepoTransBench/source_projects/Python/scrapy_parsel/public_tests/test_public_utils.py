import pytest
from parsel import utils

def test_to_unicode_int_input():
    assert utils.to_unicode(6789) == "6789"

def test_to_unicode_byte_input():
    assert utils.to_unicode(b"NewTest") == "NewTest"

def test_to_unicode_str_input():
    assert utils.to_unicode("UnicodeStringTest") == "UnicodeStringTest"

def test_to_unicode_error():
    class A:
        pass
    with pytest.raises(TypeError):
        utils.to_unicode(A())