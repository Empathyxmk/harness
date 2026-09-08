from src.picasso.okhttp3_downloader import OkHttp3Downloader

def test_public_ctor_with_cache_dir():
    file = "/tmp/public_ctor_cache"
    OkHttp3Downloader(file)
    # Only for exception check

def test_public_ctor_with_cache_dir_and_max_size():
    file = "/tmp/public_ctor_cache2"
    OkHttp3Downloader(file, 2048)
    # Only for exception check

def test_public_ctor_with_max_size():
    OkHttp3Downloader(8192)
    # Only for exception check