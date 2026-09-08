class ForeverRetryPolicy:
    def should_retry(self, attempt):
        return True

def test_should_retry_after_different_attempt():
    attempt = 42
    policy = ForeverRetryPolicy()
    should_retry = policy.should_retry(attempt)
    assert should_retry, "Should always retry regardless of attempt (public test)"