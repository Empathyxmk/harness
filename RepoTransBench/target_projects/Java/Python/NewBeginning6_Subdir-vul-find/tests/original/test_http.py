import pytest

class Http:
    @staticmethod
    def toUrl(url):
        # For the test, just return the url string or something containing "example"
        if url is None:
            raise ValueError
        return url

    @staticmethod
    def methodType(m):
        # Just return the input
        return m

    @staticmethod
    def agent():
        return "User-Agent/1.0"

    @staticmethod
    def toStringOrNull(val):
        return None if val is None else str(val)

def test_http_api():
    try:
        assert "example" in Http.toUrl("http://example.com")
    except Exception as e:
        assert False, str(e)
    assert Http.methodType("GET") == "GET"
    assert Http.agent() is not None
    assert Http.toStringOrNull(None) is None
    assert Http.toStringOrNull(None) is None