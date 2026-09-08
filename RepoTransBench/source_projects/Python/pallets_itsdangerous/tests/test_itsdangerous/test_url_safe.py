import pytest
from itsdangerous import URLSafeSerializer, BadSignature

def test_urlsafe_serializer_roundtrip():
    s = URLSafeSerializer("urlsecret")
    data = {"k": "v"}
    token = s.dumps(data)
    assert isinstance(token, str)
    assert s.loads(token) == data

def test_urlsafe_serializer_separators():
    s = URLSafeSerializer("secret", salt="mysalt")
    token = s.dumps({"x": 100})
    assert isinstance(token, str)
    assert s.loads(token) == {"x": 100}

def test_urlsafe_serializer_bad_signature():
    s = URLSafeSerializer("othersecret")
    with pytest.raises(BadSignature):
        s.loads("badbadbad")

def test_urlsafe_serializer_return_payload():
    s = URLSafeSerializer("secret")
    token = s.dumps({"val": 4})
    assert s.loads(token, return_payload=True) == {"val": 4}