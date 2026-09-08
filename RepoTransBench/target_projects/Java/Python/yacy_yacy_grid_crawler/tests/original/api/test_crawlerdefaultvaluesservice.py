import pytest

# Dummy implementation of CrawlerDefaultValuesService and needed classes
class Query:
    def __init__(self, dummy=None):
        pass

class ServiceResponse:
    def __init__(self, json_obj):
        self._json = json_obj
    def toJSON(self):
        return self._json

class CrawlerDefaultValuesService:
    defaultValues = {
        "crawlingDepth": 3,
        "mustmatch": ".*",
        "user_id": "default",
        "crawlingURL": "http://default.url"
    }
    defaultValues_clone = defaultValues.copy()
    @staticmethod
    def crawlStartDefaultClone():
        return dict(CrawlerDefaultValuesService.defaultValues)
    def getAPIPath(self):
        return "/api/defaultValues.json"
    def serviceImpl(self, q, unused):
        return ServiceResponse(dict(CrawlerDefaultValuesService.defaultValues))

def test_get_api_path():
    service = CrawlerDefaultValuesService()
    assert service.getAPIPath().endswith("/defaultValues.json")

def test_crawl_start_default_clone():
    original = CrawlerDefaultValuesService.defaultValues
    clone = CrawlerDefaultValuesService.crawlStartDefaultClone()
    for key in original:
        assert str(original[key]) == str(clone[key])
    assert original is not clone

def test_service_impl_returns_default_values():
    service = CrawlerDefaultValuesService()
    resp = service.serviceImpl(Query(), None)
    assert resp is not None
    jsonval = resp.toJSON()
    for key in CrawlerDefaultValuesService.defaultValues:
        assert str(CrawlerDefaultValuesService.defaultValues[key]) == str(jsonval[key])