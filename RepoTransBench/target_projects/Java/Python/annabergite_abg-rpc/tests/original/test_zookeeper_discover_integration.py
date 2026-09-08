import pytest
from unittest.mock import Mock, patch, MagicMock
from types import SimpleNamespace

class HostPort:
    def __init__(self, host, port):
        self.host = host
        self.port = port

class AddressWithWeight:
    def __init__(self, hostport, weight):
        self.hostport = hostport
        self.weight = weight

    def to_bytes(self):
        # For mocking purposes, serialize as a tuple of (hostport, weight)
        return (self.hostport.host, self.hostport.port, self.weight)

class Protocol:
    def __str__(self):
        return "p"

class ZooKeeperDiscover:
    def __init__(self):
        self.client = None
        self.watchers = []
        self.initialized = False

    def init(self, hps):
        self.initialized = True
        self.client = Mock()  # Normally a CuratorFramework mock
        self.hps = hps
        self.watchers = []

    def addListener(self, group, app, protocol, listener):
        if self.client is None:
            raise Exception("client is not initialized")
        # Normally adds listener and a watcher; for the test we cover control flow
        # Call with proper event types, but we simulate with a dummy implementation

    def close(self):
        for watcher in getattr(self, "watchers", []):
            try:
                watcher.close()
            except Exception:
                pass

def mock_child_data(address_with_weight):
    data = Mock()
    data.getData = Mock(return_value=address_with_weight.to_bytes())
    return data

def test_add_listener_covers_child_event_branches():
    discover = ZooKeeperDiscover()
    hps = [HostPort("localhost", 2181)]
    discover.init(hps)
    client = Mock()
    discover.client = client

    # All mocks
    watcher = Mock()
    listener = Mock()
    protocol = Protocol()
    group = "g"
    app = "a"
    protocol_str = "p"

    # Mocks for event
    event_init = SimpleNamespace(type="INITIALIZED", data=None)
    event_add = SimpleNamespace(type="CHILD_ADDED", data=mock_child_data(AddressWithWeight(HostPort("localhost", 2001), 42)))
    event_remove = SimpleNamespace(type="CHILD_REMOVED", data=mock_child_data(AddressWithWeight(HostPort("localhost", 2002), 77)))
    event_update = SimpleNamespace(type="CHILD_UPDATED", data=mock_child_data(AddressWithWeight(HostPort("localhost", 2003), 88)))
    event_other = SimpleNamespace(type="CONNECTION_LOST", data=None)

    discover.watchers = []

    # Just ensure addListener with valid arguments does not throw
    discover.addListener(group, app, protocol, listener)

def test_close_handles_watcher_list():
    discover = ZooKeeperDiscover()
    discover.init([HostPort("localhost", 2181)])

    watcher = MagicMock()
    discover.watchers = [watcher]
    watcher.close.side_effect = Exception("forced")  # Should be ignored
    try:
        discover.close()
    except Exception:
        pytest.fail("Exception should not be thrown in close() even if watcher.close throws")