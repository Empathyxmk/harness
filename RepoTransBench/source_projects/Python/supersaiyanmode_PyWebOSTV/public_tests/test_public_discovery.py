import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import pywebostv.discovery as discovery

def test_read_location_public():
    # Give different response string
    resp = "random: entry\nLocation: http://192.168.0.101/device.xml\nAnother: entry"
    result = discovery.read_location(resp)
    assert result == "http://192.168.0.101/device.xml"

def test_read_location_bytes_public():
    resp = b"something: test\nlocation: http://10.0.0.201/xml\nsomething: else"
    result = discovery.read_location(resp)
    assert result == "http://10.0.0.201/xml"

def test_validate_location_public(monkeypatch):
    # Dummy content returned with keyword to match
    class FakeResponse:
        content = b"mockabc"
    def fake_get(location, timeout=None):
        return FakeResponse()
    monkeypatch.setattr(discovery.requests, "get", fake_get)
    assert discovery.validate_location("http://test", b"abc", timeout=1) is True
    assert discovery.validate_location("http://test", b"zzz", timeout=1) is False

def test_discover_public(monkeypatch):
    # Simulate that a single host is found
    class FakeSocket:
        def __init__(self, responses):
            self.responses = responses
            self.recv_idx = 0
            self.timeout = False
        def setsockopt(self, *args, **kwargs): pass
        def settimeout(self, val): pass
        def sendto(self, msg, group): pass
        def recv(self, bufsize):
            if self.recv_idx > 0 or not self.responses:
                from socket import timeout
                raise timeout()
            self.recv_idx += 1
            return self.responses.pop(0)
        def close(self): pass

    fake_resp = (b"Location: http://192.0.2.10/some.xml\nOther: xyz",)
    def fake_socket(*args, **kwargs):
        return FakeSocket(list(fake_resp))
    monkeypatch.setattr(discovery.socket, "socket", fake_socket)
    monkeypatch.setattr(discovery, "validate_location", lambda l, k, timeout=5: True)

    found = discovery.discover("urn:test", keyword=None, hosts=True, retries=1, timeout=1, mx=1)
    # Should be a set with just the hostname from urlparse
    assert found == {"192.0.2.10"}