import pytest

class InetAddress:
    def __init__(self, address, port):
        self._address = address
        self._port = port
        self._initialized = address != "" and port != 0
    def initialized(self):
        return self._initialized
    def address(self):
        return self._address
    def port(self):
        return self._port
    def __eq__(self, other):
        return isinstance(other, InetAddress) and \
               self.address() == other.address() and \
               self.port() == other.port()

def test_inet_address_constructs_with_different_ipv4_address_and_port():
    addr_public = InetAddress("192.168.2.123", 8765)
    assert addr_public.initialized()
    assert addr_public.address() == "192.168.2.123"
    assert addr_public.port() == 8765

def test_inet_address_copy_and_assign():
    addr1_public = InetAddress("10.10.10.10", 1111)
    addr2_public = InetAddress(addr1_public.address(), addr1_public.port())
    assert addr1_public == addr2_public