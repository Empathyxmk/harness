from ratelimit.exception import RateLimitException

def test_public_rate_limit_exception_inheritance():
    ex = RateLimitException("foo", 0.99)
    assert isinstance(ex, Exception)
    assert hasattr(ex, 'period_remaining')

def test_public_exception_str_and_value():
    ex = RateLimitException("overload", 2)
    assert str(ex) == "overload"
    assert ex.period_remaining == 2