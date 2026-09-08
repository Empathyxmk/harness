import pytest

# Dummy Crawler class for test purposes.
class CrawlerDefaultValuesService: pass
class CrawlStartService: pass

class Crawler:
    # Mimic the CRAWLER_SERVICES class array
    CRAWLER_SERVICES = [CrawlerDefaultValuesService, CrawlStartService]

def test_crawler_services_contains_expected_classes():
    has_default_values = False
    has_crawl_start = False
    for c in Crawler.CRAWLER_SERVICES:
        if c.__name__ == "CrawlerDefaultValuesService":
            has_default_values = True
        if c.__name__ == "CrawlStartService":
            has_crawl_start = True
    assert has_default_values, "CRAWLER_SERVICES should contain CrawlerDefaultValuesService"
    assert has_crawl_start, "CRAWLER_SERVICES should contain CrawlStartService"