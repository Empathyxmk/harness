from ratelimit.exception import RateLimitException

def test_public_rate_limit_exception_fields():
    e = RateLimitException("limit reached", 1.25)
    assert str(e) == "limit reached"
    assert abs(e.period_remaining - 1.25) < 1e-9