import pytest
from pynubank.utils.http import HttpClient

def test_http_client_headers_public():
    client = HttpClient()
    client.set_header("X-Custom-Header", "foobar-public")
    assert client.headers["X-Custom-Header"] == "foobar-public"
    client.remove_header("X-Custom-Header")
    assert "X-Custom-Header" not in client.headers

def test_http_client_base_url_public():
    client = HttpClient()
    client.base_url = "https://public.example.com"
    assert client.base_url.startswith("https://")

def test_http_client_repr_public():
    client = HttpClient()
    r = repr(client)
    assert "HttpClient" in r