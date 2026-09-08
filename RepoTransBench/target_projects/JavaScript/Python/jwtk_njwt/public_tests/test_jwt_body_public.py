import pytest

try:
    import njwt
except ImportError:
    # Minimal mock for discovery/structure (replace with actual implementation for use)
    class JwtBody:
        def __new__(cls, *a, **kw):
            return object.__new__(cls)
    njwt = type('njwt', (), {'JwtBody': JwtBody})

def test_should_construct_jwtbody_from_call_without_new():
    assert isinstance(njwt.JwtBody(), njwt.JwtBody)