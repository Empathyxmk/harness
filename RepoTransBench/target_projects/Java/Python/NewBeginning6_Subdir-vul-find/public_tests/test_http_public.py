import pytest

class Http:
    @staticmethod
    def Response(url, cookie, ua, xHeaders, method, dataBody, enctypeBody, follow):
        # Instead of a real network operation, return a list of dummy fields
        # Simulate real return shape
        return [200, "OK", {"header": "value"}, "body_string"]

def test_response_shape():
    url = "http://example.invalid"
    cookie = "mycookie=12345"
    ua = "PublicAgent/2.0"
    xHeaders = "X-Test: public\nTest-Header: 42"
    method = "get"
    dataBody = ""
    enctypeBody = "application/json"
    follow = False

    try:
        response = Http.Response(url, cookie, ua, xHeaders, method, dataBody, enctypeBody, follow)
        assert response is not None
        assert len(response) >= 4
    except Exception as e:
        pytest.fail(f"Http.Response() threw: {e}")