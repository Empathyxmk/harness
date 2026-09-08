import pytest
from itsdangerous import URLSafeSerializer, BadSignature

def test_urlsafe_serializer_roundtrip_public():
    s = URLSafeSerializer("urlsecretpublic")
    data = {"foo": "bar"}
    token = s.dumps(data)
    assert isinstance(token, str)
    assert s.loads(token) == data

def test_urlsafe_serializer_separators_public():
    s = URLSafeSerializer("publicsecret", salt="othersalt")
    token = s.dumps({"y": 303})
    assert isinstance(token, str)
    assert s.loads(token) == {"y": 303}

def test_urlsafe_serializer_bad_signature_public():
    s = URLSafeSerializer("newsecret")
    with pytest.raises(BadSignature):
        s.loads("notavalidtoken")

def test_urlsafe_serializer_return_payload_public():
    s = URLSafeSerializer("differentsecret")
    token = s.dumps({"val": 7})
    assert s.loads(token, return_payload=True) == {"val": 7}