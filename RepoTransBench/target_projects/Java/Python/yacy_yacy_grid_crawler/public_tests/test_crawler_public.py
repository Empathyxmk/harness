# Public test version of test_crawler.py

class CrawlerDefaultValuesService: pass
class CrawlStartService: pass

class Crawler:
    CRAWLER_SERVICES = [CrawlerDefaultValuesService, CrawlStartService]

def test_crawler_services_contains_expected_classes_public():
    has_default_values = False
    has_crawl_start = False
    for c in Crawler.CRAWLER_SERVICES:
        # Check with __name__ differently (as per Java test using getName().endsWith)
        if c.__name__.endswith("DefaultValuesService"):
            has_default_values = True
        if c.__name__.endswith("CrawlStartService"):
            has_crawl_start = True
    assert has_default_values, "CRAWLER_SERVICES should contain DefaultValuesService"
    assert has_crawl_start, "CRAWLER_SERVICES should contain CrawlStartService"