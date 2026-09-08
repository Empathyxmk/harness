import pytest
from unittest.mock import Mock

class HostPort:
    def __init__(self, host, port):
        self.host = host
        self.port = port

class Protocol:
    pass

class DiscoverListener:
    def changed(self, path):
        pass

class ZooKeeperDiscover:
    def __init__(self):
        self.client = None
        self.initialized = False

    def init(self, hps):
        self.client = True
        self.initialized = True

    def addListener(self, group, app, protocol, listener):
        if listener is None:
            raise TypeError("Listener cannot be None")
        if self.client is None:
            raise Exception("Client is None")

def test_init_and_add_listener_null_check():
    discover = ZooKeeperDiscover()
    discover.init([HostPort("localhost", 2181)])
    protocol = Mock()

    # Listener is None → should raise
    with pytest.raises(TypeError):
        discover.addListener("grp", "app", protocol, None)

def test_add_listener_no_init():
    discover = ZooKeeperDiscover()
    protocol = Mock()
    listener = Mock()
    # Not called init, so client is None
    with pytest.raises(Exception):
        discover.addListener("grp", "app", protocol, listener)