import pytest
from ratelimit.exception import RateLimitException

def test_ratelimit_exception_message_and_period():
    e = RateLimitException("limit reached", 4.5)
    assert isinstance(e, RateLimitException)
    assert e.period_remaining == 4.5
    assert str(e) == "limit reached"