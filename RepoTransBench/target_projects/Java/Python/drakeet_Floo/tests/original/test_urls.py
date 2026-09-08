def test_scheme_is_floo():
    class URLs:
        @staticmethod
        def scheme():
            return "floo"
        WEB = "https://m.drakeet.me/web"
        NOT_REGISTERED = "floo://m.drakeet.me/not_registered"
    assert URLs.scheme() == "floo"

def test_url_constants():
    class URLs:
        WEB = "https://m.drakeet.me/web"
        NOT_REGISTERED = "floo://m.drakeet.me/not_registered"
    assert URLs.WEB == "https://m.drakeet.me/web"
    assert URLs.NOT_REGISTERED == "floo://m.drakeet.me/not_registered"