import pytest
from tiddl.api import ApiError


def test_ApiError_message_and_status_public():
    err = ApiError(status=420, message="Enhance Your Calm", userMessage="Slow Down")
    assert "Enhance" in str(err)
    assert err.status == 420
    assert err.userMessage == "Slow Down"


def test_ApiError_repr_has_all_fields_public():
    err = ApiError(status=405, userMessage="Not Allowed", errorCode=77, subStatus=9)
    s = repr(err)
    assert "errorCode" in s
    assert "77" in s
    assert "userMessage" in s
    assert "Not Allowed" in s
    assert "subStatus" in s
    assert "9" in s