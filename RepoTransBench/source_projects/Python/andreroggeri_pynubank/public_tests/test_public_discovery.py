from pynubank.utils.discovery import Discovery

def test_discovery_urls_public():
    d = Discovery()
    url = d.get_url('auth_api')
    assert isinstance(url, str)
    assert 'https://' in url

def test_discovery_cache_public():
    d = Discovery()
    # For public test, call twice to check repeat is OK
    url1 = d.get_url('bills_summary')
    url2 = d.get_url('bills_summary')
    assert url1 == url2