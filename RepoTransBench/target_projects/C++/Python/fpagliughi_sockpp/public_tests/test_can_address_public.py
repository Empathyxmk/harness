import pytest

class CANAddress:
    def __init__(self, iface=None):
        self._iface = iface
        self._index = None
        self._initialized = False
        if isinstance(iface, str):
            if iface == "":
                self._initialized = False
            elif iface.startswith("vcan") or iface.startswith("can"):
                self._initialized = True
                self._iface = iface
                try:
                    self._index = int(iface[4:])
                except Exception:
                    self._index = 1
            else:
                self._initialized = False
        elif isinstance(iface, int):
            self._index = iface
            self._iface = "can"+str(iface)
            self._initialized = True

    def initialized(self):
        return self._initialized
    def interface(self):
        return self._iface
    def index(self):
        return self._index

def test_can_address_with_different_valid_interface_name():
    addr_public = CANAddress("vcan1")
    assert addr_public.initialized()
    assert addr_public.interface() == "vcan1"

def test_can_address_with_an_empty_interface():
    addr_public = CANAddress("")
    assert not addr_public.initialized()

def test_can_address_with_numeric_interface_index_different():
    addr_public = CANAddress(3)
    assert addr_public.initialized()
    assert addr_public.index() == 3