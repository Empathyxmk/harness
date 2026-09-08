import pytest

# Simulations for the Trivia2 public proxy upgrade tests

class ImplementationV1Pub:
    def __init__(self):
        self.val = None

    def setValue(self, v):
        self.val = v
        return Receipt()

    def value(self):
        return self.val

class ImplementationV2Pub(ImplementationV1Pub):
    def __init__(self):
        super().__init__()
        self.addr = None

    def setAddr(self, addr):
        self.addr = addr
        return Receipt()

    def addr_(self):
        return self.addr

class TransparentProxyPub:
    def __init__(self, impl_address):
        self.implementation = impl_address

    def getImplementation(self):
        return self.implementation

    def upgradeTo(self, new_impl_addr):
        self.implementation = new_impl_addr
        return Receipt()

class UniversalProxyPub(TransparentProxyPub):
    pass

class Receipt:
    def wait(self):
        pass

@pytest.fixture(scope="function")
def transparent_proxy():
    # Deploy v1
    ImplementationV1_addr = "0xImplV1Pub"
    ImplementationV1_inst = ImplementationV1Pub()
    Proxy = TransparentProxyPub(ImplementationV1_addr)
    Instance = ImplementationV1_inst
    return Proxy, Instance, ImplementationV1_inst

@pytest.fixture(scope="function")
def universal_proxy():
    ImplementationV1_addr = "0xUniImplV1Pub"
    ImplementationV1_inst = ImplementationV1Pub()
    Proxy = UniversalProxyPub(ImplementationV1_addr)
    Instance = ImplementationV1_inst
    return Proxy, Instance, ImplementationV1_inst

def behaves_like_implementation_v1_pub(instance):
    # Simulate setting a unique value for public
    instance.setValue("99")
    assert instance.value() == "99"

def behaves_like_implementation_v2_pub(instance):
    instance.setAddr("0x0000000000000000000000000000000000000099")
    assert instance.addr_() == "0x0000000000000000000000000000000000000099"

def test_transparent_proxy_public():
    Proxy, Instance, ImplementationV1_inst = transparent_proxy
    assert Proxy.getImplementation() == "0xImplV1Pub"

    behaves_like_implementation_v1_pub(Instance)

    # Upgrade to V2 (using public-specific addresses)
    ImplementationV2_addr = "0xImplV2Pub"
    ImplementationV2_inst = ImplementationV2Pub()
    Proxy.upgradeTo(ImplementationV2_addr)
    InstanceV2 = ImplementationV2_inst
    assert Proxy.getImplementation() == "0xImplV2Pub"

    behaves_like_implementation_v1_pub(InstanceV2)
    behaves_like_implementation_v2_pub(InstanceV2)

def test_universal_proxy_public():
    Proxy, Instance, ImplementationV1_inst = universal_proxy
    assert Proxy.getImplementation() == "0xUniImplV1Pub"

    behaves_like_implementation_v1_pub(Instance)

    # Upgrade to V2 (using public-specific addresses)
    ImplementationV2_addr = "0xUniImplV2Pub"
    ImplementationV2_inst = ImplementationV2Pub()
    Proxy.upgradeTo(ImplementationV2_addr)
    InstanceV2 = ImplementationV2_inst
    assert Proxy.getImplementation() == "0xUniImplV2Pub"

    behaves_like_implementation_v1_pub(InstanceV2)
    behaves_like_implementation_v2_pub(InstanceV2)