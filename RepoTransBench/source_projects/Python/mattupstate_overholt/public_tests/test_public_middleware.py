import overholt.middleware

def test_public_middleware_module_exists():
    # Public, different: test that module defines an attribute
    assert hasattr(overholt.middleware, "__doc__")