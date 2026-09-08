from ratelimit.exception import RateLimitException

def test_rate_limit_exception_fields():
    e = RateLimitException("too many", 3.5)
    assert str(e) == "too many"
    assert e.period_remaining == 3.5