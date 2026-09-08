def test_import_fetcher():
    from yahoo_historical import Fetcher
    assert Fetcher is not None
    f = Fetcher("aapl", 1600000000, 1600001000)
    assert hasattr(f, 'get_historical')