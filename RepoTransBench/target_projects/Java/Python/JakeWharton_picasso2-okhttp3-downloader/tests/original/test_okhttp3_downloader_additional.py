import pytest
import tempfile
import os

from src.picasso.okhttp3_downloader import OkHttp3Downloader

def test_load_succeeds_with_different_network_policies():
    downloader = OkHttp3Downloader()
    assert downloader.load("http://localhost/ok", 0) is not None
    assert downloader.load("http://localhost/ok", -1) is not None
    assert downloader.load("http://localhost/ok", 123) is not None

def test_shutdown_multiple_times():
    downloader = OkHttp3Downloader()
    downloader.shutdown()
    downloader.shutdown()  # Should not throw

def test_load_throws_when_url_is_empty():
    downloader = OkHttp3Downloader()
    with pytest.raises(IOError):
        downloader.load("", 0)

def test_all_constructors_with_shutdown():
    # Using directory path as string rather than File
    d1 = OkHttp3Downloader("/tmp/cacheA", 5)
    d2 = OkHttp3Downloader("/tmp/cacheB")
    d3 = OkHttp3Downloader(123)
    d4 = OkHttp3Downloader()
    d5 = OkHttp3Downloader("dummy2")
    for d in [d1, d2, d3, d4, d5]:
        d.shutdown()