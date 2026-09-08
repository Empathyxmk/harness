import pytest
from fuzzywuzzy import process

def test_public_process_warning(caplog):
    """Check that a string reduced to 0 by processor logs a warning to stderr"""

    query = '......'
    choices = ['......']
    with caplog.at_level("WARNING"):
        _ = process.extractOne(query, choices)
    assert any(
        "Applied processor reduces input query to empty string" in m
        for m in caplog.messages
    )