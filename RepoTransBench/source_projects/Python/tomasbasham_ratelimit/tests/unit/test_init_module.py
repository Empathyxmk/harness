import ratelimit

def test_init_module_all_exports():
    # Ensure __all__ includes all public API
    for name in ratelimit.__all__:
        assert hasattr(ratelimit, name)

def test_init_limits_and_rate_limited_are_decorator():
    assert ratelimit.limits is ratelimit.RateLimitDecorator
    assert ratelimit.rate_limited is ratelimit.RateLimitDecorator
    assert callable(ratelimit.limits)
    assert callable(ratelimit.rate_limited)

def test_version_string_exists():
    v = ratelimit.__version__
    assert isinstance(v, str)
    assert "." in v