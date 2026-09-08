import pytest
import cloudconvert.signed_url as signed_url

def test_generate_signed_url_with_path(monkeypatch):
    # monkeypatch depending imports
    monkeypatch.setattr(signed_url, "SECRET_KEY", "sekrit")
    monkeypatch.setattr(signed_url, "API_URL", "https://api/")
    url = signed_url.generate_signed_url("123", "test")
    assert url.startswith("https://api/")

def test_generate_signed_url_missing_key(monkeypatch):
    monkeypatch.setattr(signed_url, "SECRET_KEY", None)
    monkeypatch.setattr(signed_url, "API_URL", "https://api/")
    url = signed_url.generate_signed_url("123", "test")
    assert url is None