from src.picasso.okhttp3_downloader import OkHttp3Downloader

def test_shutdown_does_not_throw():
    downloader = OkHttp3Downloader()
    downloader.shutdown()
    # no asserts, just check no exception

def test_dummy_constructor():
    downloader = OkHttp3Downloader("dummy")
    # no asserts, just check for exceptions