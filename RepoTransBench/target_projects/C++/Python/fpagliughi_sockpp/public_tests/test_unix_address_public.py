import pytest

class UnixAddress:
    def __init__(self, path):
        self._path = path
        self._initialized = bool(path)
    def initialized(self):
        return self._initialized
    def path(self):
        return self._path

def test_unix_address_with_different_valid_path():
    addr_public = UnixAddress("/tmp/test_public_sock")
    assert addr_public.initialized()
    assert addr_public.path() == "/tmp/test_public_sock"

def test_unix_address_with_empty_string():
    addr_public = UnixAddress("")
    assert not addr_public.initialized()