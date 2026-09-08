def test_scheme_is_floo_public():
    class URLs:
        @staticmethod
        def scheme():
            return "floo"
        WEB = "https://m.drakeet.me/web"
        NOT_REGISTERED = "floo://m.drakeet.me/not_registered"
    assert URLs.scheme() == "floo"

def test_constants_public():
    class URLs:
        WEB = "https://m.drakeet.me/web"
        NOT_REGISTERED = "floo://m.drakeet.me/not_registered"
    assert URLs.WEB != "https://not-public-url.com"
    assert URLs.NOT_REGISTERED != "floo://not/public"
    assert URLs.WEB.startswith("https://")
    assert URLs.NOT_REGISTERED.startswith("floo://")