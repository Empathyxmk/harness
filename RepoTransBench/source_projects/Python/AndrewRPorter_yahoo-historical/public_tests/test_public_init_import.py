def test_import_fetcher_public():
    # Use a different ticker, different timestamps
    from yahoo_historical import Fetcher
    assert Fetcher is not None
    # Different symbol, different time period
    f = Fetcher("msft", 1650000000, 1650001000)
    assert hasattr(f, 'get_historical')