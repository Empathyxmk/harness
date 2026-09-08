import pytest
from yahoo_historical.fetch import Fetcher
import time

TEST_TICKER = "AAPL"
TIME_START = int(time.mktime((2017, 1, 1, 0, 0, 0, 0, 0, 0)))
TIME_END = int(time.mktime((2017, 1, 4, 0, 0, 0, 0, 0, 0)))

def mock_get_historical(self, kind="history", as_dataframe=True):
    if as_dataframe:
        class DummyDf:
            def __getitem__(self, key):
                return [1,2,3]
        return DummyDf()
    else:
        return "col1,col2\n1,2\n3,4"

def test_get_no_dataframe(monkeypatch):
    monkeypatch.setattr(Fetcher, "_get", lambda self, kind, as_dataframe=True: "col1,col2\n1,2\n3,4")
    data = Fetcher(TEST_TICKER, TIME_START, TIME_END).get_historical(as_dataframe=False)
    assert "col1" in data

def test_get_with_lowercase(monkeypatch):
    monkeypatch.setattr(Fetcher, "_get", mock_get_historical)
    data = Fetcher(TEST_TICKER.lower(), TIME_START, TIME_END).get_historical()
    assert hasattr(data, "__getitem__")

def test_get_historical(monkeypatch):
    monkeypatch.setattr(Fetcher, "_get", mock_get_historical)
    data = Fetcher(TEST_TICKER, TIME_START, TIME_END).get_historical()
    assert hasattr(data, "__getitem__")

def test_invalid_date(monkeypatch):
    monkeypatch.setattr(Fetcher, "_get", mock_get_historical)
    with pytest.raises(Exception):
        Fetcher(TEST_TICKER, "invalid_date", TIME_END).get_historical()

def test_fetcher_with_float_dates(monkeypatch):
    monkeypatch.setattr(Fetcher, "_get", mock_get_historical)
    start = float(TIME_START)
    end = float(TIME_END)
    f = Fetcher(TEST_TICKER, start, end)
    assert hasattr(f.get_historical(), "__getitem__")