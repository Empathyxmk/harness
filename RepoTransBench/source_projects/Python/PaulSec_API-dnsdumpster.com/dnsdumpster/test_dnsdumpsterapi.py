import pytest
from dnsdumpster import DNSDumpsterAPI

class DummyResponse:
    def __init__(self, text, status_code=200):
        self.text = text
        self.status_code = status_code
        self.headers = {}

@pytest.fixture
def invalid_html():
    return "<html><body>No form here!</body></html>"

def test_dnsdumpsterapi_init():
    api = DNSDumpsterAPI()
    assert hasattr(api, 'session')

def test_dnsdumpsterapi_search_usage(monkeypatch):
    api = DNSDumpsterAPI()
    monkeypatch.setattr(api.session, "get", lambda url: DummyResponse("<html><form></form></html>"))
    # DNSDumpsterAPI.search expects a domain argument, here we mock the POST too
    def dummy_post(url, data, headers):
        return DummyResponse("<html><table></table></html>")
    monkeypatch.setattr(api.session, "post", dummy_post)
    result = api.search("example.com")
    assert isinstance(result, dict)

def test_dnsdumpsterapi_search_no_csrf(monkeypatch, invalid_html):
    api = DNSDumpsterAPI()
    monkeypatch.setattr(api.session, "get", lambda url: DummyResponse(invalid_html))
    with pytest.raises(Exception):
        api.search("example.com")

def test_dnsdumpsterapi_form_parsing(monkeypatch):
    # Test BeautifulSoup parsing logic for forms/inputs (csrf check)
    api = DNSDumpsterAPI()
    html = '''
    <html>
    <form>
      <input type="hidden" name="csrfmiddlewaretoken" value="12345"/>
      <input type="text" name="targetip" value="example.com"/>
    </form>
    </html>
    '''
    monkeypatch.setattr(api.session, "get", lambda url: DummyResponse(html))
    def dummy_post(url, data, headers):
        return DummyResponse("<html><table></table></html>")
    monkeypatch.setattr(api.session, "post", dummy_post)
    api.search("example.com")