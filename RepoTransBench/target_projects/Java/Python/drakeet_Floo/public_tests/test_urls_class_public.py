def test_urls_is_web_scheme_with_http_public():
    def is_web_scheme(url):
        return url.startswith("http://") or url.startswith("https://")
    assert is_web_scheme("http://floo.io")

def test_urls_is_web_scheme_with_custom_scheme_public():
    def is_web_scheme(url):
        return url.startswith("http://") or url.startswith("https://")
    assert not is_web_scheme("notweb://example.org")

def test_urls_combine_public():
    def combine(prefix, path):
        if prefix.endswith("/"):
            prefix = prefix.rstrip("/")
        return prefix + "/" + path
    assert combine("foo://bar", "baz") == "foo://bar/baz"