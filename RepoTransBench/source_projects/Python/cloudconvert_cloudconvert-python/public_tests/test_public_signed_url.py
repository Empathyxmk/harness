import pytest
import cloudconvert.signed_url as signed_url

def test_generate_signed_url_with_path_public(monkeypatch):
    # monkeypatch depending imports with DIFFERENT key/url
    monkeypatch.setattr(signed_url, "SECRET_KEY", "public123")
    monkeypatch.setattr(signed_url, "API_URL", "https://public-api/")
    url = signed_url.generate_signed_url("999", "sample")
    assert url.startswith("https://public-api/")

def test_generate_signed_url_missing_key_public(monkeypatch):
    monkeypatch.setattr(signed_url, "SECRET_KEY", "")
    monkeypatch.setattr(signed_url, "API_URL", "https://public-api/")
    url = signed_url.generate_signed_url("456", "demo")
    assert url is None