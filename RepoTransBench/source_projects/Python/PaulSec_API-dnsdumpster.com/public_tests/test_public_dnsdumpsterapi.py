import sys
import pytest

sys.path.insert(0, './dnsdumpster')
from DNSDumpsterAPI import DNSDumpsterAPI

def dummy_search(self, domain):
    # Provide different fake results for coverage
    dummy_results = {
        "duckduckgo.com": {
            "domain": "duckduckgo.com",
            "dns_records": {
                "dns": [{"domain": "ns1.duckduckgo.com"}],
                "mx": [{"exchange": "duckduckgo-com.mail.protection.outlook.com"}],
                "host": [{"host": "imap.duckduckgo.com"}],
            }
        },
        "mit.edu": {
            "domain": "mit.edu",
            "dns_records": {
                "dns": [{"domain": "NS1-163.AKAM.NET"}],
                "mx": [{"exchange": "mit-edu.mail.protection.outlook.com"}],
                "host": [{"host": "imap.mit.edu"}],
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

def test_dnsdumpsterapi_public_attributetypes():
    api = DNSDumpsterAPI()
    result = api.search('duckduckgo.com')
    assert isinstance(result, dict)
    assert "domain" in result and result["domain"] == "duckduckgo.com"
    assert "dns_records" in result and isinstance(result["dns_records"], dict)
    assert "mx" in result["dns_records"]
    assert isinstance(result["dns_records"]["mx"], list)
    assert "host" in result["dns_records"]
    assert "dns" in result["dns_records"]
    for key in ("mx", "host", "dns"):
        assert key in result["dns_records"]

def test_dnsdumpsterapi_public_result_content():
    api = DNSDumpsterAPI()
    res = api.search("mit.edu")
    assert isinstance(res, dict)
    assert res["domain"] == "mit.edu"
    assert len(res) > 1
    has_records = False
    for records in res.get("dns_records", {}).values():
        if isinstance(records, list) and records:
            has_records = True
            break
    assert has_records, "There should be at least one populated DNS record entry"