import pytest
from yahoo_historical.fetch import Fetcher
import time

TEST_TICKER_PUBLIC = "GOOG"
TIME_START_PUBLIC = int(time.mktime((2018, 2, 1, 0, 0, 0, 0, 0, 0)))
TIME_END_PUBLIC = int(time.mktime((2018, 2, 5, 0, 0, 0, 0, 0, 0)))

def test_get_historical_public(monkeypatch):
    monkeypatch.setattr(Fetcher, "_get", lambda self, kind, as_dataframe=True: "open,close\n5,6\n7,8")
    fetcher = Fetcher(TEST_TICKER_PUBLIC, TIME_START_PUBLIC, TIME_END_PUBLIC)
    result = fetcher.get_historical(as_dataframe=False)
    assert "open" in result

def test_repr_str_public():
    fetcher = Fetcher(TEST_TICKER_PUBLIC, TIME_START_PUBLIC, TIME_END_PUBLIC)
    r = repr(fetcher)
    s = str(fetcher)
    assert "Fetcher" in r and "GOOG" in r
    assert "Fetcher" in s and "GOOG" in s

def test_get_history_with_kwargs_public(monkeypatch):
    monkeypatch.setattr(Fetcher, "_get", lambda self, kind, as_dataframe=True: "public_test")
    fetcher = Fetcher(TEST_TICKER_PUBLIC, TIME_START_PUBLIC, TIME_END_PUBLIC)
    assert fetcher.get_historical(as_dataframe=False) == "public_test"

def test_get_dividend_and_split_public(monkeypatch):
    # If the methods exist in this Fetcher, should not raise; if not, AttributeError.
    fetcher = Fetcher(TEST_TICKER_PUBLIC, TIME_START_PUBLIC, TIME_END_PUBLIC)
    if hasattr(fetcher, "get_dividend"):
        with pytest.raises(Exception):
            fetcher.get_dividend()
        with pytest.raises(Exception):
            fetcher.get_split()
    else:
        with pytest.raises(AttributeError):
            fetcher.get_dividend()
        with pytest.raises(AttributeError):
            fetcher.get_split()

def test_keyerror_public(monkeypatch):
    class RaiseKeyError:
        def __call__(self, kind, as_dataframe=True):
            raise KeyError("fail-public")
    monkeypatch.setattr(Fetcher, "_get", RaiseKeyError())
    fetcher = Fetcher(TEST_TICKER_PUBLIC, TIME_START_PUBLIC, TIME_END_PUBLIC)
    with pytest.raises(KeyError):
        fetcher.get_historical()

def test_wrong_ticker_public():
    with pytest.raises(Exception):
        Fetcher("!!!", int(time.mktime((2019,3,4,0,0,0,0,0,0))), int(time.mktime((2019,3,5,0,0,0,0,0,0)))).get_historical()