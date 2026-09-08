import pytest
from cppstddb import database_error, vertical_print

def test_basic_constructor():
    err = database_error("Something went wrong")
    assert err.message() == "Something went wrong"
    assert err.retcode() == 0
    assert err.driver_message() == ""
    assert "Something went wrong" in str(err)

def test_retcode_constructor():
    err = database_error("Oops", 42)
    assert err.message() == "Oops"
    assert err.retcode() == 42
    assert err.driver_message() == ""
    assert "retcode: 42" in str(err)

def test_full_constructor():
    err = database_error("Err", 105, "driver details")
    assert err.message() == "Err"
    assert err.retcode() == 105
    assert err.driver_message() == "driver details"
    assert "driver_message: driver details" in str(err)

def test_vertical_print(capsys):
    err = database_error("print test", 99, "drv msg")
    from io import StringIO
    oss = StringIO()
    vertical_print(oss, err)
    s = oss.getvalue()
    assert "database error" in s
    assert "print test" in s
    assert "99" in s
    assert "drv msg" in s