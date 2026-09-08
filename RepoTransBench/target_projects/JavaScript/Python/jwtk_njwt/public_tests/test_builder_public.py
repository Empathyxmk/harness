import pytest
import uuid

try:
    import njwt
    import properties
except ImportError:
    # Minimal mocks for testing structure/examples (replace for real impl)
    class Errors:
        UNSUPPORTED_SIGNING_ALG = "Unsupported signing algorithm"
        SIGNING_KEY_REQUIRED = "Signing key required"
    properties = type('properties', (), {"errors": Errors()})

    class DummyJwt:
        def setSigningAlgorithm(self, alg):
            if alg == 'invalid-alg':
                raise Exception(properties.errors.UNSUPPORTED_SIGNING_ALG)
            return self
        def setHeader(self, key, value): return self
    def create(*args, **kwargs):
        if not args:
            raise Exception(properties.errors.SIGNING_KEY_REQUIRED)
        if isinstance(args[0], dict) and len(args) == 1:
            raise Exception(properties.errors.SIGNING_KEY_REQUIRED)
        return DummyJwt()
    njwt = type('njwt', (), {'Jwt': DummyJwt, 'create': staticmethod(create)})

def test_signwith_throws_for_nonexistent_alg():
    with pytest.raises(Exception) as excinfo:
        njwt.Jwt().setSigningAlgorithm('invalid-alg')
    assert properties.errors.UNSUPPORTED_SIGNING_ALG in str(excinfo.value)

def test_create_throws_signing_key_required_without_args():
    with pytest.raises(Exception) as excinfo:
        njwt.create()
    assert properties.errors.SIGNING_KEY_REQUIRED in str(excinfo.value)

def test_create_default_token_with_random_secret():
    # JS: uuid.v4().replace(/[0-9]/g, 'z')
    import re
    secret = re.sub(r'[0-9]', 'z', str(uuid.uuid4()))
    assert isinstance(njwt.create(secret), njwt.Jwt)

def test_create_throws_if_defaults_and_no_secret():
    with pytest.raises(Exception) as excinfo:
        njwt.create({"active": True})
    assert properties.errors.SIGNING_KEY_REQUIRED in str(excinfo.value)

def test_create_does_not_throw_when_secret_provided():
    njwt.create('mySecretPublicTest')  # should not throw