from src.picasso.okhttp3_downloader import OkHttp3Downloader

def test_ctor_with_another_cache_dir():
    file = "/tmp/pub_cache_c"
    OkHttp3Downloader(file)
    # Only for exception check

def test_ctor_with_another_cache_dir_and_max_size():
    file = "/tmp/pub_cache_d"
    OkHttp3Downloader(file, 5555)
    # Only for exception check

def test_ctor_with_another_max_size():
    OkHttp3Downloader(9876)
    # Only for exception check