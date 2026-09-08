from src.picasso.okhttp3_downloader import OkHttp3Downloader

def test_shutdown_is_safe_repeatedly():
    downloader = OkHttp3Downloader()
    downloader.shutdown()
    downloader.shutdown()
    # Still no exception

def test_another_dummy_constructor():
    OkHttp3Downloader("publicValue")
    # Just for construction