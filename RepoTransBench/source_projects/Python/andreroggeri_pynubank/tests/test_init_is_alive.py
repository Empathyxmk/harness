import pytest
from pynubank import is_alive
from pynubank.utils.http import HttpClient

def test_is_alive_default(monkeypatch):
    called = []
    orig = HttpClient.raw_get

    def fake(self, url):
        called.append(True)
        class R:
            status_code = 200
            def __init__(self, url):
                self.url = url
        return R(url)
    monkeypatch.setattr(HttpClient, "raw_get", fake)
    try:
        assert is_alive() is True
    finally:
        HttpClient.raw_get = orig