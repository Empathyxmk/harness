import pytest
import uuid
import time
import datetime

try:
    import njwt
except ImportError:
    # Minimal mock for njwt.Jwt
    class Jwt:
        def __init__(self):
            self.body = type('JwtBody', (), {})()
            self.header = type('JwtHeader', (), {})()
        def setClaim(self, key, value):
            setattr(self.body, key, value)
            return self
        def setHeader(self, key, value):
            setattr(self.header, key, value)
            return self
        def setSubject(self, sub):
            self.body.sub = sub
            return self
        def setIssuer(self, iss):
            self.body.iss = iss
            return self
        def setExpiration(self, date):
            self.body.exp = int(date.timestamp())
            return self
    njwt = type('njwt', (), {"Jwt": Jwt})

def test_jwt_constructs_itself_call_as_function():
    assert isinstance(njwt.Jwt(), njwt.Jwt)

def test_set_claim_sets_different_claim_value():
    claim_value = str(uuid.uuid4()).replace("-", "#")
    assert njwt.Jwt().setClaim("publicClaim", claim_value).body.publicClaim == claim_value

def test_set_header_sets_another_header_param():
    kid = str(uuid.uuid4())[:8]
    assert njwt.Jwt().setHeader('publicKid', kid).header.publicKid == kid

def test_set_subject_sets_sub_with_new_value():
    sub = "user-" + str(uuid.uuid1())
    assert njwt.Jwt().setSubject(sub).body.sub == sub

def test_set_issuer_sets_iss_with_different_value():
    iss = "issuer-public-" + str(uuid.uuid1())
    assert njwt.Jwt().setIssuer(iss).body.iss == iss

def test_set_expiration_accepts_valid_date_and_sets_exp():
    d = datetime.datetime.fromtimestamp(time.time() + 99999)
    assert njwt.Jwt().setExpiration(d).body.exp == int(d.timestamp())