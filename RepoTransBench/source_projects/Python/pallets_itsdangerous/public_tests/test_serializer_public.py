import pytest
from itsdangerous import Serializer, BadSignature, BadPayload

def test_serializer_roundtrip_public():
    s = Serializer("a_different_key")
    d = {"gamma": 13, "zeta": [5, 4]}
    token = s.dumps(d)
    # itsdangerous default is string output unless return_bytes=True
    assert isinstance(token, str)
    assert s.loads(token) == d

def test_serializer_roundtrip_with_custom_serializer_public():
    import json
    class CustomJSON:
        def dumps(self, obj):
            # Valid JSON, just use different spacing
            return json.dumps(obj, separators=(",", ":"))
        def loads(self, s):
            return json.loads(s)
    s = Serializer("k3y_public!", serializer=CustomJSON())
    token = s.dumps({"foo": 100})
    assert s.loads(token) == {"foo": 100}

def test_serializer_invalid_payload_public():
    s = Serializer("testkey")
    # This triggers BadSignature not BadPayload since signature fails first
    with pytest.raises(BadSignature):
        s.loads("$%anotherinvalidpayload$%")

def test_serializer_bad_signature_public():
    s = Serializer("keyxxx")
    with pytest.raises(BadSignature):
        s.loads("totallyinvalidsignature-publictest")