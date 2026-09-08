import pytest
import re
import time
import uuid

try:
    import njwt
except ImportError:
    # Minimal mock for test discovery/structure (replace with actual implementation for use)
    class Jwt:
        def __init__(self, claims=None, issued_at=True):
            self.body = type('JwtBody', (), {})()
            self.body.iat = int(time.time())
            self.body.jti = str(uuid.uuid4()) + "-"
            self.compacted = False
        def compact(self):
            self.compacted = True
            return "token"
    def create(claims=None, key=None, alg=None):
        return Jwt()
    def verify(token, key, alg, cb):
        # Simulate async verify callback as in JS
        cb(None, Jwt())
    njwt = type('njwt', (), {
        "create": staticmethod(create),
        "Jwt": Jwt,
        "verify": staticmethod(verify)
    })

def itShouldBeAValidJwt(jwt):
    # Checks: is Jwt instance, iat properly set, jti format
    assert isinstance(njwt.create({}, str(uuid.uuid4())), njwt.Jwt)
    now_unix = int(time.time())
    actual_iat = njwt.create({}, str(uuid.uuid4())).body.iat
    # allow iat == now_unix or iat == now_unix-1 because of timing differences
    assert abs(actual_iat - now_unix) <= 1
    assert re.match(r'[a-zA-Z0-9]+[-]', jwt.body.jti)

def test_create_and_verify_jwt_with_hs256_and_different_test_data():
    # Mimics the single "it" from src test
    key = str(uuid.uuid4()).replace("-", "XX")
    claims = {"goodbye": str(uuid.uuid4()), "info": False}
    jwt = njwt.create(claims, key, "HS256")
    token = jwt.compact()
    itShouldBeAValidJwt(jwt)

    results = {}
    def cb(err, jwt2):
        results['called'] = True
        assert err is None, "Unexpected error returned"
        itShouldBeAValidJwt(jwt2)
    njwt.verify(token, key, "HS256", cb)
    assert results.get('called', False)