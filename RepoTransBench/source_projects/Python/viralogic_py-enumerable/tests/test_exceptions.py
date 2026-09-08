import pytest
from py_linq import exceptions

def test_exceptions_instantiation():
    e1 = exceptions.NoElementsError("msg")
    assert isinstance(e1, Exception)
    e2 = exceptions.NullArgumentError("msg2")
    assert isinstance(e2, Exception)
    e3 = exceptions.NoMatchingElement("msg3")
    assert isinstance(e3, Exception)
    e4 = exceptions.MoreThanOneMatchingElement("msg4")
    assert isinstance(e4, Exception)