import pytest
import pywebostv.discovery as discovery
import types

class FakeResp:
    def __init__(self, msg):
        self.msg = msg
    def decode(self, encoding):
        return self.msg

def test_read_location_bytes_and_str():
    # Test with bytes input
    msg = b"LOCATION: http://somewhere/\nOther: xx"
    result = discovery.read_location(msg)
    assert result == "http://somewhere/"

    # Test with str input with mixed case
    msg = "Location: http://foo/bar\n"
    result = discovery.read_location(msg)
    assert result == "http://foo/bar"

    # No location header
    assert discovery.read_location("no-location-here") is None

def test_validate_location_true_false(monkeypatch):
    class Resp:
        def __init__(self, content):
            self.content = content
    # Should succeed if keyword is in content
    monkeypatch.setattr(discovery.requests, "get", lambda url, timeout=5: Resp(b"abc"))
    assert discovery.validate_location("irrelevant", b"abc")
    # Should fail if keyword is not in content
    assert not discovery.validate_location("irrelevant", b"zzz")
    # Should return True if keyword is Falsy (None or empty string)
    assert discovery.validate_location("irrelevant", b"", timeout=1)
    # Handle request exception
    def raise_ex(url, timeout=5): raise discovery.requests.exceptions.RequestException("err")
    monkeypatch.setattr(discovery.requests, "get", raise_ex)
    assert discovery.validate_location("irrelevant", b"any") is False

def test_discover(monkeypatch):
    # Patch socket.socket so we can simulate responses
    fake_recv_calls = []
    class FakeSock:
        def __init__(self):
            self.calls = 0
        def setsockopt(self, *a): pass
        def settimeout(self, t): pass
        def sendto(self, msg, group): fake_recv_calls.append((msg, group))
        def recv(self, sz):
            if self.calls == 0:
                self.calls += 1
                msg = b"LOCATION: http://tv_host/test\nAnother: val"
                return msg
            raise timeout_exc
        def close(self): pass
    class timeout_exc(Exception): pass

    import socket as orig_socket
    monkeypatch.setattr(discovery.socket, "socket", lambda *a, **k: FakeSock())
    monkeypatch.setattr(discovery, "read_location", lambda data: "http://tv_host/test" if b"LOCATION" in data or "LOCATION" in data.decode("utf8", "ignore") else None)
    monkeypatch.setattr(discovery, "validate_location", lambda url, kw, timeout=5: True)
    monkeypatch.setattr(discovery.socket, "timeout", timeout_exc)
    monkeypatch.setattr(discovery, "urlparse", lambda u: types.SimpleNamespace(hostname="tv_host"))

    # Return host version
    hosts = discovery.discover("urn:lge:service:webos-second-screen", keyword=None, hosts=True, retries=1)
    assert hosts == {"tv_host"}
    # Return location version
    monkeypatch.setattr(discovery, "urlparse", lambda u: types.SimpleNamespace(hostname="tv_host"))
    urls = discovery.discover("service", keyword=None, hosts=False, retries=1)
    assert urls == {"http://tv_host/test"}