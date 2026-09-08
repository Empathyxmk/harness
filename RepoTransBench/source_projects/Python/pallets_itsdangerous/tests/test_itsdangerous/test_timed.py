import time
import pytest
from itsdangerous import TimedSerializer, SignatureExpired, BadTimeSignature, BadSignature

def test_timedserializer_dumps_loads():
    s = TimedSerializer("secret-key")
    data = {"msg": "timed"}
    dumped = s.dumps(data)
    loaded = s.loads(dumped)
    assert loaded == data

def test_timedserializer_expiry():
    s = TimedSerializer("secret-expiry")
    data = {"foo": 1}
    token = s.dumps(data)
    assert s.loads(token) == data
    # Should be expired, using max_age=0 and a past timestamp
    with pytest.raises(SignatureExpired):
        s.loads(token, max_age=-1)

def test_timedserializer_tuple_loading_options():
    s = TimedSerializer("secret-key2")
    token = s.dumps({"a": 2})
    # loads(..., return_timestamp=True) returns (data, timestamp)
    result = s.loads(token, return_timestamp=True)
    assert isinstance(result, tuple)
    assert result[0] == {"a": 2}
    # Accepting both float and datetime for timestamp, depending on itsdangerous version
    import datetime
    assert isinstance(result[1], (float, datetime.datetime))

def test_timedserializer_bad_signature():
    s = TimedSerializer("secret")
    # A completely broken token, missing '.' separator
    with pytest.raises(BadSignature):
        s.loads("bad-token")

    # Validly signed but purposely altered token
    orig = s.dumps({"foo": 42})
    tampered = orig[::-1]  # Definitely not the same!
    with pytest.raises(BadTimeSignature):
        s.loads(tampered)