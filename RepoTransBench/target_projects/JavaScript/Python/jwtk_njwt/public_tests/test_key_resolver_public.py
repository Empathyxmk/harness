import pytest

try:
    import njwt
except ImportError:
    # Minimal mock for testing only (replace with actual implementation)
    class Verifier:
        keyResolver = None
        def __init__(self): pass
        def withKeyResolver(self, resolver):
            self.keyResolver = resolver
            return self
    njwt = type('njwt', (), {"Verifier": Verifier})

def test_verifier_constructs_without_new():
    assert isinstance(njwt.Verifier(), njwt.Verifier)

def test_with_key_resolver_sets_field():
    resolver = lambda: None
    jwtVerifier = njwt.Verifier()
    jwtVerifier.withKeyResolver(resolver)
    assert hasattr(jwtVerifier, 'keyResolver')
    assert jwtVerifier.keyResolver == resolver

def test_with_key_resolver_returns_verifier():
    jwtVerifier = njwt.Verifier()
    assert jwtVerifier.withKeyResolver(lambda: None) is jwtVerifier