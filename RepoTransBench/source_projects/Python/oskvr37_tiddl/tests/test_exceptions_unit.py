import pytest
from tiddl.exceptions import ApiError

def test_ApiError_str_repr_fields():
    # Test with all fields
    err = ApiError(status=404, subStatus=0, userMessage='not found', errorCode=999, message='msg')
    assert "404" in str(err)
    assert "not found" in repr(err)
    assert err.status == 404
    assert err.errorCode == 999
    assert err.subStatus == 0
    assert err.userMessage == "not found"
    assert err.message == "msg"

def test_ApiError_missing_fields():
    # Test with missing and default fields
    err = ApiError(status=401, userMessage=None)
    assert err.status == 401
    assert err.subStatus is None or err.subStatus == 0
    assert "userMessage" in repr(err)
    # Should not raise

def test_ApiError_only_status():
    err = ApiError(status=502)
    assert err.status == 502

def test_ApiError_with_kwargs():
    err = ApiError(status=123, foo="bar", custom="cval")
    assert hasattr(err, "foo") and hasattr(err, "custom")
    assert err.foo == "bar"
    assert err.custom == "cval"