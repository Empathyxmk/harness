import pytest
from itsdangerous.exc import (
    BadData,
    BadSignature,
    BadTimeSignature,
    SignatureExpired,
    BadHeader,
    BadPayload,
)
from datetime import datetime, timezone

def test_bad_data_str_and_message():
    err = BadData("msg-1")
    assert str(err) == "msg-1"
    assert err.message == "msg-1"

def test_bad_signature_payload():
    err = BadSignature("fail sig", payload="abc")
    assert str(err) == "fail sig"
    assert err.payload == "abc"

def test_bad_time_signature_payload_and_date():
    dt = datetime.now(timezone.utc)
    err = BadTimeSignature("fail time sig", payload="bbb", date_signed=dt)
    assert err.message == "fail time sig"
    assert err.payload == "bbb"
    assert err.date_signed == dt

def test_signature_expired_is_subclass():
    assert issubclass(SignatureExpired, BadTimeSignature)

def test_bad_header_payload_and_error():
    orig_ex = Exception("boom")
    bh = BadHeader("bad head", payload="yy", header={"x":"y"}, original_error=orig_ex)
    assert bh.message == "bad head"
    assert bh.payload == "yy"
    assert bh.header == {"x":"y"}
    assert bh.original_error == orig_ex

def test_bad_payload_original_error():
    orig_ex = ValueError("failz")
    bp = BadPayload("bad pay", original_error=orig_ex)
    assert bp.message == "bad pay"
    assert bp.original_error == orig_ex