import pytest
from src.picasso.okhttp3_downloader import OkHttp3Downloader

def test_load_succeeds_with_other_network_policies():
    downloader = OkHttp3Downloader()
    assert downloader.load("http://127.0.0.1/success", 1) is not None
    assert downloader.load("http://127.0.0.1/success", 42) is not None
    assert downloader.load("http://127.0.0.1/success", -100) is not None

def test_shutdown_many_times():
    downloader = OkHttp3Downloader()
    downloader.shutdown()
    downloader.shutdown()
    downloader.shutdown()  # Should not throw, extra shutdown

def test_load_throws_when_url_is_null_string():
    downloader = OkHttp3Downloader()
    with pytest.raises(IOError):
        downloader.load(None, 0)

def test_all_constructors_with_shutdown_public():
    d1 = OkHttp3Downloader("/tmp/pub_cacheA", 15)
    d2 = OkHttp3Downloader("/tmp/pub_cacheB")
    d3 = OkHttp3Downloader(321)
    d4 = OkHttp3Downloader()
    d5 = OkHttp3Downloader("publicDummy")
    for d in [d1, d2, d3, d4, d5]:
        d.shutdown()