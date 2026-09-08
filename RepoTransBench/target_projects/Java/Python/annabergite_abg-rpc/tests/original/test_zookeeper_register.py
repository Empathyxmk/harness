import pytest
from unittest.mock import Mock

class HostPort:
    def __init__(self, host, port):
        self.host = host
        self.port = port

class Protocol:
    pass

class ZooKeeperRegister:
    def __init__(self):
        self.client = None
        self.initialized = False

    def init(self, hps):
        self.client = True
        self.initialized = True

    def register(self, group, app, protocol, server_addr, idx):
        if self.client is None:
            raise Exception("Client is None in register")
        # Simulated registration logic

def test_init_and_register_null_check():
    register = ZooKeeperRegister()
    register.init([HostPort("localhost", 2181)])
    protocol = Mock()
    server_addr = HostPort("127.0.0.1", 9876)
    tmp = ZooKeeperRegister()
    # Not initialized, so should raise
    with pytest.raises(Exception):
        tmp.register("g", "a", protocol, server_addr, 1)