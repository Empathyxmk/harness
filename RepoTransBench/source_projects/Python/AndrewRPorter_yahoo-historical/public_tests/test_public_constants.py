def test_constants_fields_public():
    from yahoo_historical import constants
    # Ensure API_URL, DATE_INTERVALS, ONE_DAY_INTERVAL are available (but check different values than in original)
    assert hasattr(constants, "API_URL")
    assert hasattr(constants, "DATE_INTERVALS")
    assert hasattr(constants, "ONE_DAY_INTERVAL")
    # Check at least one different valid interval is present
    assert "1d" in getattr(constants, "DATE_INTERVALS")
    assert constants.ONE_DAY_INTERVAL == "1d"

def test_api_url_format_public():
    from yahoo_historical.constants import API_URL
    # Use different but valid public test values
    url = API_URL % ("TSLA", 1610000000, 1610020000, "1d", "history")
    assert "TSLA" in url and "16100" in url and "1d" in url
    history_pos = url.find("history")
    assert history_pos > 0