import time
import pytest
from itsdangerous import TimedSerializer, BadTimeSignature, SignatureExpired, BadSignature

def test_timed_serializer_roundtrip_public():
    s = TimedSerializer("pubtimedkey")
    data = {"index": 333}
    token = s.dumps(data)
    assert isinstance(token, str)
    assert s.loads(token) == data

def test_timed_serializer_with_max_age_public():
    s = TimedSerializer("pubtimedkey")
    data = {"val": 17}
    token = s.dumps(data)
    assert s.loads(token, max_age=3) == data

def test_timed_serializer_bad_signature_public():
    s = TimedSerializer("pubk2")
    # Token missing required signature separator, triggers BadSignature
    with pytest.raises(BadSignature):
        s.loads("definitely_invalid_token")  # purposely missing '.'

def test_timed_signature_expired_public():
    s = TimedSerializer("expirepub")
    data = {"test": True}
    token = s.dumps(data)
    time.sleep(1)
    with pytest.raises(SignatureExpired):
        s.loads(token, max_age=0)