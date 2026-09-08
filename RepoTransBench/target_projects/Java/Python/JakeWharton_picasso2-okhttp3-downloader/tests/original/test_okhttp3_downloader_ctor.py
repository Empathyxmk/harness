from src.picasso.okhttp3_downloader import OkHttp3Downloader

def test_no_arg_ctor():
    OkHttp3Downloader()
    # no asserts, just check for exceptions