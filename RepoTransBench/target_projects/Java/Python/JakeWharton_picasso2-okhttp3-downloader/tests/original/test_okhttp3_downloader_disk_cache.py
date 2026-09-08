from src.picasso.okhttp3_downloader import OkHttp3Downloader

def test_ctor_with_cache_dir():
    file = "/tmp/cache"
    OkHttp3Downloader(file)
    # no asserts, just check for exceptions

def test_ctor_with_cache_dir_and_max_size():
    file = "/tmp/cache"
    OkHttp3Downloader(file, 1024)
    # no asserts, just check for exceptions

def test_ctor_with_max_size():
    OkHttp3Downloader(4096)
    # no asserts, just check for exceptions