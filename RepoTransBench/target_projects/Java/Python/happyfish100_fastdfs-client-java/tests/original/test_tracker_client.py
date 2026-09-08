from unittest import mock

class DummyConnection:
    pass

class DummyTrackerGroup:
    def __init__(self):
        self.tracker_servers = []

    def getTrackerServer(self, *args):
        return self.tracker_servers[0] if self.tracker_servers else None

    def getTrackerServer1(self, idx):
        if len(self.tracker_servers) > idx:
            return self.tracker_servers[idx]
        return None

class DummyTrackerServer:
    def __init__(self, connection=None, idx=0):
        self.connection = connection if connection else DummyConnection()
        self._idx = idx

    def getConnection(self):
        return self.connection

    def getIndex(self):
        return self._idx

class TrackerClient:
    def __init__(self, group=None):
        self.tracker_group = group or DummyTrackerGroup()
        self.errno = 0

    def getErrorCode(self):
        return self.errno

    def getTrackerServer(self):
        return self.tracker_group.getTrackerServer()

    def getConnection(self, server):
        if server:
            return server.getConnection()
        servers = self.tracker_group.tracker_servers
        last_exc = None
        for idx, s in enumerate(servers):
            try:
                return s.getConnection()
            except Exception as e:
                last_exc = e
        if last_exc:
            raise last_exc
        return None

def test_constructors_and_get_error_code():
    group = DummyTrackerGroup()
    client = TrackerClient(group)
    assert client.tracker_group is group
    defaultClient = TrackerClient()
    assert defaultClient.getErrorCode() == 0

def test_get_tracker_server():
    group = DummyTrackerGroup()
    srv = DummyTrackerServer()
    group.tracker_servers = [srv]
    group.getTrackerServer = lambda: srv
    client = TrackerClient(group)
    assert client.getTrackerServer() is srv

def test_get_connection_success():
    group = DummyTrackerGroup()
    server = DummyTrackerServer()
    group.tracker_servers = [server]
    client = TrackerClient(group)
    assert client.getConnection(server) == server.connection

def test_get_connection_with_failover():
    group = DummyTrackerGroup()
    server1 = DummyTrackerServer()
    server2 = DummyTrackerServer()
    # Make server1.getConnection fail
    orig_fn = server1.getConnection
    server1.getConnection = mock.Mock(side_effect=Exception("fail!"))
    group.tracker_servers = [server1, server2]
    client = TrackerClient(group)
    assert client.getConnection(None) == server2.connection