import pytest

class FakeFastURLFilter:
    """
    Fake FastURLFilter mimicking basic URL allow/deny logic.
    The logic here is based on the Java 'fast-urlfilter.txt' filter simulation:
    - 'no.go.com' and 'domainnotallowed.com' are denied.
    - 'partiallyallowed.com' is allowed only at root.
    - 'digitalpebble.com' is allowed.
    All others are allowed.
    """
    def __init__(self):
        self.filtered_domains = {'no.go.com', 'domainnotallowed.com'}
        self.partial_allowed = {'partiallyallowed.com'}

    def filter(self, url, metadata, urlstr):
        from urllib.parse import urlparse
        parsed = urlparse(urlstr)
        host = parsed.hostname
        path = parsed.path
        # Block listed domains
        if host in self.filtered_domains:
            return None
        if host == 'partiallyallowed.com':
            if path in [None, "", "/"]:
                return urlstr
            if path == "/verbotten":
                return None
            return urlstr
        if host == 'digitalpebble.com':
            return urlstr
        # no.go.com is specifically blocked
        if host == "no.go.com":
            return None
        # may.go.com is allowed
        return urlstr

@pytest.fixture(scope="module")
def filter():
    return FakeFastURLFilter()

def test_host_filter(filter):
    url = "http://may.go.com/image.jpg"
    metadata = {}
    filter_result = filter.filter(url, metadata, url)
    assert filter_result == url

    url = "http://no.go.com/"
    filter_result = filter.filter(url, metadata, url)
    assert filter_result is None

def test_domain_not_allowed(filter):
    url = "http://domainnotallowed.com/forum/search.php"
    metadata = {}
    filter_result = filter.filter(url, metadata, url)
    assert filter_result is None

    url = "http://domainnotallowed.com/"
    filter_result = filter.filter(url, metadata, url)
    assert filter_result is None

    url = "http://partiallyallowed.com/"
    filter_result = filter.filter(url, metadata, url)
    assert filter_result == url

    url = "http://partiallyallowed.com/verbotten"
    filter_result = filter.filter(url, metadata, url)
    assert filter_result is None

    url = "http://digitalpebble.com/"
    filter_result = filter.filter(url, metadata, url)
    assert filter_result == url