import pytest
from yahoo_historical import fetch
import time

def test_fetcher_create_url_public():
    f = fetch.Fetcher("NFLX", 1500000000, 1500500000)
    url = f.create_url("history")
    assert "NFLX" in url
    assert "history" in url

def test_fetcher_invalid_interval_public():
    f = fetch.Fetcher("NFLX", 1510000000, 1510500000, interval="8h")
    # Patch requests.get so it does not try real
    with pytest.raises(ValueError):
        # forcibly trigger the ValueError for an unsupported interval
        f.get_historical()

def test_fetcher_get_historical_dataframe_public(monkeypatch):
    import pandas as pd
    data_csv = "a,b\n1,2\n3,4"
    monkeypatch.setattr(fetch.Fetcher, "create_url", lambda self, event: "http://test-url/")
    class FakeResp:
        def __init__(self): self.content = data_csv.encode("utf-8")
    monkeypatch.setattr(fetch.requests, "get", lambda url, headers={}: FakeResp())
    f = fetch.Fetcher("AMZN", 1550000000, 1550600000)
    df = f.get_historical()
    assert isinstance(df, pd.DataFrame)
    assert "a" in df.columns and "b" in df.columns
    assert df.iloc[0]["a"] == 1