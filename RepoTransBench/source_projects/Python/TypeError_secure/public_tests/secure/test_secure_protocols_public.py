import pytest
from secure.secure import HeadersProtocol, SetHeaderProtocol, Secure

class AlternateHeadersObj:
    def __init__(self):
        self.headers = {"X-Test": "abc"}

class AlternateSetHeaderObj:
    def __init__(self):
        self.was_called = False
        self.k = self.v = None
    def set_header(self, k, v):
        self.was_called = True
        self.k = k
        self.v = v

def test_headers_protocol_public():
    o = AlternateHeadersObj()
    assert isinstance(o, HeadersProtocol)
    not_hdrs = 42
    assert not isinstance(not_hdrs, HeadersProtocol)

def test_set_header_protocol_public():
    o = AlternateSetHeaderObj()
    assert isinstance(o, SetHeaderProtocol)
    not_set = []
    assert not isinstance(not_set, SetHeaderProtocol)

def test_secure_response_protocol_headers_public():
    # Use a different header type than original
    from secure.headers.strict_transport_security import StrictTransportSecurity
    s = Secure(hsts=StrictTransportSecurity().max_age(777))
    dummy_resp = AlternateHeadersObj()
    # Just check that Secure has headers_list and correct type
    assert hasattr(s, "headers_list")
    assert isinstance(s.headers_list[0], StrictTransportSecurity)