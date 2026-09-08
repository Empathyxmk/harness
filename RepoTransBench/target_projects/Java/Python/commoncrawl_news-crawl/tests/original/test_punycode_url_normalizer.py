import pytest
import idna

class PunycodeURLNormalizer:
    def filter(self, _1, _2, url):
        from urllib.parse import urlparse, urlunparse, quote, unquote
        try:
            parsed = urlparse(url)
            host = parsed.hostname
            if host is None:
                return None
            try:
                ascii_host = host.encode('ascii')
                # already punycode, check if it's an ascii hostname
                return url
            except UnicodeEncodeError:
                punycode_host = idna.encode(host).decode('ascii')
            # Rebuild the URL with punycode host
            scheme = parsed.scheme
            netloc = punycode_host
            if parsed.port:
                netloc += f":{parsed.port}"
            if parsed.username:
                if parsed.password:
                    netloc = f"{parsed.username}:{parsed.password}@{netloc}"
                else:
                    netloc = f"{parsed.username}@{netloc}"
            path = parsed.path
            params = parsed.params
            query = parsed.query
            fragment = parsed.fragment
            rebuilt = urlunparse((scheme, netloc, path, params, query, fragment))
            return rebuilt
        except Exception:
            return None

@pytest.fixture(scope='module')
def normalizer():
    return PunycodeURLNormalizer()

def test_ascii_url(normalizer):
    url = "http://example.com"
    assert normalizer.filter(None, None, url) == url

def test_punycode_url(normalizer):
    url = "http://例え.テスト"
    result = normalizer.filter(None, None, url)
    assert result.startswith("http://xn--r8jz45g.xn--zckzah")

def test_non_host_part_is_not_changed(normalizer):
    url = "http://täst.de/foo?ä=ö"
    result = normalizer.filter(None, None, url)
    # Only the host should be punycoded, rest stays
    assert result.startswith("http://xn--tst-qla.de")
    assert "/foo" in result
    assert "?" in result

def test_malformed_url(normalizer):
    url = "not a url"
    assert normalizer.filter(None, None, url) is None

def test_host_already_punycode(normalizer):
    url = "http://xn--fsq.xn--0zwm56d"
    assert normalizer.filter(None, None, url) == url