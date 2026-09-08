import pytest
from pynubank.nubank import Nubank

def test_should_use_http_client_if_none_is_provided(monkeypatch):
    # Patch Discovery to avoid real HTTP request
    class FakeDiscovery:
        def __init__(self, client):
            pass
        def discover(self):
            return {}

    monkeypatch.setattr('pynubank.utils.discovery.Discovery', FakeDiscovery)
    nubank_client = Nubank()
    assert isinstance(nubank_client, Nubank)