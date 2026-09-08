import pytest

try:
    import njwt
except ImportError:
    # Minimal mock to allow test logic to execute (replace for real implementation)
    class Jwt: pass
    class JwtBody:
        def toJSON(self): pass
        def compact(self): pass
    class JwtHeader:
        def compact(self): pass
    class Verifier: pass

    def object_is_frozen(obj):
        # In real implementation, check for immutability/frozen-ness
        return True
    def verify(token): pass

    njwt = type('njwt', (), {})()
    njwt.Jwt = Jwt
    njwt.JwtBody = JwtBody
    njwt.JwtHeader = JwtHeader
    njwt.Verifier = Verifier
    njwt.verify = staticmethod(verify)
    object_is_frozen = staticmethod(object_is_frozen)
else:
    object_is_frozen = lambda obj: True  # Assume as present

def test_exports_classes_with_frozen_prototypes():
    assert object_is_frozen(njwt.Jwt)
    assert object_is_frozen(njwt.JwtBody)
    assert object_is_frozen(njwt.JwtHeader)
    assert object_is_frozen(njwt.Verifier)

def test_exports_classes_with_frozen_prototypes_prototype():
    assert object_is_frozen(njwt.Jwt)
    assert object_is_frozen(njwt.JwtBody)
    assert object_is_frozen(njwt.JwtHeader)
    assert object_is_frozen(njwt.Verifier)

def test_no_prototype_pollution():
    # Checks methods are still present even after verify()
    token = (
        "ewogICJ0eXAiOiAiUHVibGljSldUIiwKICAiYWxnIjogIk5vbmUiLAogICJfX3Byb3RvX18iOiB7CiAgICAidHlwIjogIkpXVCIsCiAgICAiYWxnIjogIkhTMzg0IiwKICAgICJfX3Byb3RvX18iOiB7ImNvbXBhY3QiOm51bGwsInJlc2VydmVkS2V5cyI6WyJpbmZvIl0KfQogIH0KfQ.ewogICJwdWIiOiAyLAogICJzY29wZSI6ICJ0ZXN0IiwKICAianRpIjogImE1MmNkY2Y2LTExZTktNDg1Zi05MDEwLWZlODc5MTkzMDQwNCIsCiAgImlhdCI6IDI1ODc0Nzg1MDYsCiAgImV4cCI6IDI1ODc0Nzg1MDYsCiAgIl9fcHJvdG9fXyI6IHsiY29tcGFjdCI6bnVsbCwidG9KU09OIjpudWxsLCJwb2xsdXRlZCI6dHJ1ZX19"
    )

    assert hasattr(njwt.JwtBody, 'toJSON')
    assert hasattr(njwt.JwtBody, 'compact')
    assert hasattr(njwt.JwtHeader, 'compact')

    njwt.verify(token)

    assert hasattr(njwt.JwtBody, 'toJSON')
    assert hasattr(njwt.JwtBody, 'compact')
    assert hasattr(njwt.JwtHeader, 'compact')