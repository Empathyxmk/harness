import pytest
import socket

class SockAddress:
    def __init__(self, family=None, address=None, size=None):
        self._family = family
        self._initialized = family is not None
    def initialized(self):
        return self._initialized
    def family(self):
        return self._family
    def __eq__(self, other):
        if isinstance(other, SockAddress):
            return (self._family, self._initialized) == (other._family, other._initialized)
        return False

def test_sock_address_default_constructed_is_not_initialized():
    addr_public = SockAddress()
    assert not addr_public.initialized()

def test_sock_address_from_family_works_different_family():
    addr_public = SockAddress(socket.AF_UNIX, None, 0)
    assert addr_public.initialized()
    assert addr_public.family() == socket.AF_UNIX

def test_sock_address_copy_construction_and_equality_different():
    addr1_public = SockAddress(socket.AF_INET, None, 0)
    addr2_public = SockAddress(addr1_public.family())
    addr2_public._initialized = addr1_public._initialized
    assert addr1_public == addr2_public