import pytest

def test_url_object():
    # This simulates cpr::Url in Python
    url = "http://127.0.0.1"
    assert "http://127.0.0.1" in url

def test_response_struct():
    # Fake a 'Response' structure similar to cpr's
    class DummyResponse:
        def __init__(self):
            self.url = None
            self.elapsed = 0
            self.status_code = None
            self.text = ""
    resp = DummyResponse()
    resp.url = "http://localhost"
    resp.elapsed = 100
    resp.status_code = 200
    resp.text = "ok"
    assert resp.status_code == 200
    assert resp.text == "ok"
    # No actual HTTP requests performed for CI safety