import pytest
from src.picasso.okhttp3_downloader import OkHttp3Downloader

def test_load_throws_on_null_url():
    downloader = OkHttp3Downloader()
    with pytest.raises(IOError):
        downloader.load(None, 0)

def test_load_throws_on_invalid_url():
    downloader = OkHttp3Downloader()
    with pytest.raises(IOError):
        downloader.load("ftp://localhost/abc", 0)

def test_load_succeeds_on_valid_url():
    downloader = OkHttp3Downloader()
    result = downloader.load("http://localhost/abc", 0)
    assert result is not None