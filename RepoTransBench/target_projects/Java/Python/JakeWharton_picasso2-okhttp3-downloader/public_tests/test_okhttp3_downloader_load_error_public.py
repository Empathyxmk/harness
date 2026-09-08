import pytest
from src.picasso.okhttp3_downloader import OkHttp3Downloader

def test_load_throws_on_invalid_protocol():
    downloader = OkHttp3Downloader()
    with pytest.raises(IOError):
        downloader.load("ftp://someurl", 0)  # Should throw, not 'http'