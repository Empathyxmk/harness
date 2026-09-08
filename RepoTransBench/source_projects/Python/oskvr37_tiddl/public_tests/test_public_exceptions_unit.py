import pytest
from tiddl.exceptions import ApiError

def test_ApiError_str_repr_fields_public():
    # Use different numbers and messages
    err = ApiError(status=400, subStatus=99, userMessage='bad request', errorCode=1234, message='err occurred')
    assert "400" in str(err)
    assert "bad request" in repr(err)
    assert err.status == 400
    assert err.errorCode == 1234
    assert err.subStatus == 99
    assert err.userMessage == "bad request"
    assert err.message == "err occurred"

def test_ApiError_missing_fields_public():
    err = ApiError(status=403, userMessage="denied")
    assert err.status == 403
    assert err.userMessage == "denied"
    # subStatus is None or zero per implementation
    assert err.subStatus is None or err.subStatus == 0
    assert "userMessage" in repr(err)

def test_ApiError_only_status_public():
    err = ApiError(status=500)
    assert err.status == 500

def test_ApiError_with_other_kwargs_public():
    err = ApiError(status=321, custom_field="xyz", another="val")
    assert hasattr(err, "custom_field") and hasattr(err, "another")
    assert err.custom_field == "xyz"
    assert err.another == "val"