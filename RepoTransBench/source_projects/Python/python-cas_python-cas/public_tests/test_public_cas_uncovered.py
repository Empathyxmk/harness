import pytest

@pytest.mark.skip(reason="Test requires network access; skipping public variant as well.")
def test_get_proxy_ticket_custom_public():
    # Skipped in public tests, mirrors skip in private test.
    pass

@pytest.mark.skip(reason="Test requires network access; skipping public variant as well.")
def test_some_other_network_test_public():
    # Skipped in public tests, mirrors skip in private test.
    pass