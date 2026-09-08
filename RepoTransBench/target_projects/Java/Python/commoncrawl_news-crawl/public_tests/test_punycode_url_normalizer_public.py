import idna
import urllib.parse
import unicodedata

def normalize(url):
    parsed = urllib.parse.urlparse(url)
    try:
        hostname = idna.encode(parsed.hostname).decode('ascii')
    except Exception:
        hostname = parsed.hostname
    def strip_accents(s):
        return ''.join(c for c in unicodedata.normalize('NFKD', s) if not unicodedata.combining(c))
    path = strip_accents(parsed.path)
    rebuilt = urllib.parse.urlunparse((
        parsed.scheme,
        hostname,
        path,
        parsed.params,
        parsed.query,
        parsed.fragment
    ))
    return rebuilt

def test_normalizer_basic():
    idn = "http://müller.de/"
    expected = "http://xn--mller-kva.de/"
    assert normalize(idn) == expected

def test_normalizer_path():
    idn = "http://müller.de/über-uns"
    expected = "http://xn--mller-kva.de/ber-uns"
    assert normalize(idn) == expected

def test_normalizer_ascii():
    url = "http://example.com/plain"
    assert normalize(url) == url

def test_normalizer_query():
    url = "http://müller.de/search?q=über"
    expected = "http://xn--mller-kva.de/search?q=ber"
    assert normalize(url) == expected

def test_normalizer_different_idn():
    idn = "http://müller.de/über-uns"
    expected = "http://xn--mller-kva.de/ber-uns"
    assert normalize(idn) == expected