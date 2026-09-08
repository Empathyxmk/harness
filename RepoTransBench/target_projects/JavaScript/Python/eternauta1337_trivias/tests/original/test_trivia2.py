import pytest

# Mocks for contract proxies and upgrade logic

class ImplementationV1:
    def __init__(self):
        self.val = None

    def setValue(self, v):
        self.val = v
        return Receipt()

    def value(self):
        return self.val

class ImplementationV2(ImplementationV1):
    def __init__(self):
        super().__init__()
        self.addr = None

    def setAddr(self, addr):
        self.addr = addr
        return Receipt()

    def addr_(self):
        return self.addr

class TransparentProxy:
    def __init__(self, impl_address):
        self.implementation = impl_address

    def getImplementation(self):
        return self.implementation

    def upgradeTo(self, new_impl_addr):
        self.implementation = new_impl_addr
        return Receipt()

class UniversalProxy(TransparentProxy):
    pass

class Receipt:
    def wait(self):
        pass

@pytest.fixture(scope="function")
def transparent_proxy():
    # Deploy v1
    ImplementationV1_addr = "0xImplV1"
    ImplementationV1_inst = ImplementationV1()
    Proxy = TransparentProxy(ImplementationV1_addr)
    # "Contract at" pattern: interaction uses V1 interface
    Instance = ImplementationV1_inst
    return Proxy, Instance, ImplementationV1_inst

@pytest.fixture(scope="function")
def universal_proxy():
    ImplementationV1_addr = "0xUniImplV1"
    ImplementationV1_inst = ImplementationV1()
    Proxy = UniversalProxy(ImplementationV1_addr)
    Instance = ImplementationV1_inst
    return Proxy, Instance, ImplementationV1_inst

def test_transparent_proxy_behaves():
    Proxy, Instance, ImplementationV1_inst = transparent_proxy
    # implementation address set
    assert Proxy.getImplementation() == "0xImplV1"

    # v1 logic
    Instance.setValue("42")
    assert Instance.value() == "42"

    # Upgrade to V2
    ImplementationV2_addr = "0xImplV2"
    ImplementationV2_inst = ImplementationV2()

    Proxy.upgradeTo(ImplementationV2_addr)
    InstanceV2 = ImplementationV2_inst
    # v1 logic still works
    InstanceV2.setValue("42")
    assert InstanceV2.value() == "42"
    # v2 logic
    InstanceV2.setAddr("0x0000000000000000000000000000000000000042")
    assert InstanceV2.addr_() == "0x0000000000000000000000000000000000000042"
    # And the implementation pointer updated
    assert Proxy.getImplementation() == "0xImplV2"

def test_universal_proxy_behaves():
    Proxy, Instance, ImplementationV1_inst = universal_proxy
    assert Proxy.getImplementation() == "0xUniImplV1"

    # v1 logic
    Instance.setValue("42")
    assert Instance.value() == "42"

    # Upgrade to V2
    ImplementationV2_addr = "0xUniImplV2"
    ImplementationV2_inst = ImplementationV2()
    Proxy.upgradeTo(ImplementationV2_addr)

    InstanceV2 = ImplementationV2_inst
    # v1 logic still works
    InstanceV2.setValue("42")
    assert InstanceV2.value() == "42"
    # v2 logic
    InstanceV2.setAddr("0x0000000000000000000000000000000000000042")
    assert InstanceV2.addr_() == "0x0000000000000000000000000000000000000042"

    assert Proxy.getImplementation() == "0xUniImplV2"