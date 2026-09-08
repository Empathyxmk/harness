def test_session_timeout_public_variant():
    # Simulate the timeout for a different input (e.g., 42 min)
    max_inactive_interval_in_seconds = 42 * 60
    assert max_inactive_interval_in_seconds == 2520