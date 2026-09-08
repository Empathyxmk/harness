import pytest

# Mock for Uri class with minimal implementation
class Uri:
    def __init__(self):
        self._scheme = ""
        self._host = ""
        self._port = 0
        self._path = ""
        self._query = ""

    def ParseFromString(self, s):
        # A very simple/mock parse. Assumes URLs are valid and structured like http(s)://host:port/path?query
        import re
        m = re.match(r"(\w+):\/\/([^\/:]+)(?::(\d+))?([^\?]*)\??(.*)", s)
        if not m:
            return False
        self._scheme = m.group(1)
        self._host = m.group(2)
        self._port = int(m.group(3)) if m.group(3) else (0 if self._scheme == "https" else 80)
        self._path = m.group(4) if m.group(4) else ""
        self._query = m.group(5)
        return True

    def scheme(self):
        return self._scheme

    def host(self):
        return self._host

    def port(self):
        return self._port

    def path(self):
        return self._path if self._path else ""

    def query(self):
        return self._query

def test_parse_http():
    uri = Uri()
    assert uri.ParseFromString("http://newhost:9090/publicpath?foo=bar")
    assert uri.scheme() == "http"
    assert uri.host() == "newhost"
    assert uri.port() == 9090
    assert uri.path() == "/publicpath"
    assert uri.query() == "foo=bar"

def test_parse_no_port():
    uri = Uri()
    assert uri.ParseFromString("https://example.net/resource")
    assert uri.scheme() == "https"
    assert uri.host() == "example.net"
    assert uri.port() == 0
    assert uri.path() == "/resource"
    assert uri.query() == ""