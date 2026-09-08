import ratelimit

def test_public_init_module_all_exports():
    # Ensure __all__ includes all public API, but check via different attribute
    exported = set(ratelimit.__all__)
    # Pick a different assertion style
    for name in exported:
        assert getattr(ratelimit, name, None) is not None

def test_public_init_limits_and_rate_limited_are_decorator():
    # Instead of id(), use repr to confirm identical references
    assert repr(ratelimit.limits) == repr(ratelimit.RateLimitDecorator)
    assert repr(ratelimit.rate_limited) == repr(ratelimit.RateLimitDecorator)
    assert hasattr(ratelimit.limits, '__call__')
    assert hasattr(ratelimit.rate_limited, '__call__')

def test_public_version_string_length():
    v = ratelimit.__version__
    # Instead of "." in v, check for at least 2 dots (major.minor.patch)
    assert isinstance(v, str)
    assert v.count(".") >= 2