from gscholar import gscholar as gs

import pytest

@pytest.mark.xfail(reason="Google's rate limiter.")
def test_public_query():
    """A query with different input should return non empty result."""
    result = gs.query('Niels Bohr', gs.FORMAT_BIBTEX)
    assert len(result) > 0

@pytest.mark.xfail(reason="Google's rate limiter.")
def test_public_query_utf8():
    """A query using different UTF8 characters should give non empty result."""
    result = gs.query("Srinivasa Ramanujan", gs.FORMAT_BIBTEX)
    assert len(result) > 0