import sys
import types
import pytest

sys.path.insert(0, './dnsdumpster')
from DNSDumpsterAPI import DNSDumpsterAPI

class DummyResponse:
    def __init__(self, content):
        self.content = content

def dummy_search(self, domain):
    # Provide fake results for public test (domain-specific)
    dummy_results = {
        "openai.com": {
            "domain": "openai.com",
            "dns_records": {
                "dns": [{"domain": "ns1.openai.com"}],
                "mx": [{"exchange": "aspmx.l.google.com"}],
                "host": [{"host": "mail.openai.com"}],
            }
        },
        "duckduckgo.com": {
            "domain": "duckduckgo.com",
            "dns_records": {
                "dns": [{"domain": "ns1.duckduckgo.com"}],
                "mx": [{"exchange": "duckduckgo-com.mail.protection.outlook.com"}],
                "host": [{"host": "imap.duckduckgo.com"}],
            }
        }
    }
    return dummy_results.get(domain, {
        "domain": domain,
        "dns_records": {
            "dns": [],
            "mx": [],
            "host": []
        }
    })

@pytest.fixture(autouse=True)
def patch_search(monkeypatch):
    monkeypatch.setattr(DNSDumpsterAPI, "search", dummy_search)

def test_dnsdumpsterapi_public_search():
    api = DNSDumpsterAPI()
    # Domain different from common internal test examples
    result = api.search("openai.com")
    assert isinstance(result, dict)
    assert result["domain"] == "openai.com"
    assert "dns_records" in result
    assert isinstance(result["dns_records"], dict)
    assert any(result["dns_records"].get(key) for key in result["dns_records"])
    found = False
    for value in result["dns_records"].values():
        if isinstance(value, list) and value:
            found = True
            break
    assert found, "At least one DNS record list should not be empty"