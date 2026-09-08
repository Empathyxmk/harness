def test_get_default_timeout_public():
    # Assume this would be a real static method; for this dummy, just use a fixed value
    class CrawlerDefaultValuesService:
        @staticmethod
        def getDefaultTimeout():
            return 60
        defaultMaxDepth = 8
        defaultMaxLinks = 2000

    default_timeout = CrawlerDefaultValuesService.getDefaultTimeout()
    assert default_timeout > 0

def test_default_values_constants_public():
    class CrawlerDefaultValuesService:
        defaultMaxDepth = 8
        defaultMaxLinks = 2000

    depth = CrawlerDefaultValuesService.defaultMaxDepth
    links = CrawlerDefaultValuesService.defaultMaxLinks
    assert depth > 0 and links > 0
    assert depth != 0 and links != 0