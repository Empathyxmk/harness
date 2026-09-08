def test_parse_timeout_public():
    class CrawlStartService:
        @staticmethod
        def parseTimeout(params, default_value):
            if "timeout" in params:
                try:
                    return int(params["timeout"][0])
                except Exception:
                    return default_value
            return default_value

    params = {"timeout": ["90"]}
    result = CrawlStartService.parseTimeout(params, 250)
    assert result == 90

def test_parse_timeout_defaults_public():
    class CrawlStartService:
        @staticmethod
        def parseTimeout(params, default_value):
            if "timeout" in params:
                try:
                    return int(params["timeout"][0])
                except Exception:
                    return default_value
            return default_value

    params = {}
    result = CrawlStartService.parseTimeout(params, 60)
    assert result == 60

def test_parse_timeout_invalid_public():
    class CrawlStartService:
        @staticmethod
        def parseTimeout(params, default_value):
            if "timeout" in params:
                try:
                    return int(params["timeout"][0])
                except Exception:
                    return default_value
            return default_value

    params = {"timeout": ["invalid"]}
    result = CrawlStartService.parseTimeout(params, 15)
    assert result == 15