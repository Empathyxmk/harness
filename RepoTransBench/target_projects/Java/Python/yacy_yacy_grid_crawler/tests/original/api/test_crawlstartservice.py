import pytest

# Dummy class implementations
class Query:
    def __init__(self, dummy=None):
        self.data = {}
    def set(self, key, value):
        self.data[key] = value
    def get(self, key, default=None):
        return self.data.get(key, default)

class ServiceResponse:
    def __init__(self, json_obj):
        self._json = json_obj
    def toJSON(self):
        return self._json

class CrawlStartService:
    def getAPIPath(self):
        return "/api/crawlStart.json"
    def serviceImpl(self, call, unused):
        crawlingDepth = call.get("crawlingDepth", 4)
        user_id = call.get("user_id", "guest")
        # Limit crawlingDepth to max 8
        crawlingDepth = min(crawlingDepth, 8)
        out = {
            "crawlingDepth": crawlingDepth,
            "mustmatch": ".*",
            "user_id": user_id,
            "crawlingURL": "http://example.com"
        }
        return ServiceResponse(out)

def test_get_api_path():
    service = CrawlStartService()
    assert service.getAPIPath().endswith("/crawlStart.json")

def test_service_impl_returns_merged_defaults():
    service = CrawlStartService()
    call = Query()
    resp = service.serviceImpl(call, None)
    assert resp is not None
    jsonval = resp.toJSON()
    assert "crawlingDepth" in jsonval
    assert "mustmatch" in jsonval
    assert "user_id" in jsonval
    assert "crawlingURL" in jsonval

def test_service_impl_with_override():
    service = CrawlStartService()
    call = Query()
    call.set("crawlingDepth", 10)
    call.set("user_id", "user42")
    resp = service.serviceImpl(call, None)
    jsonval = resp.toJSON()
    assert jsonval["crawlingDepth"] == 8  # max cap
    assert jsonval["user_id"] == "user42"