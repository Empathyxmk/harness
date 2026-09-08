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

def test_constructors_and_get_error_code_public():
    group = DummyTrackerGroup()
    client = TrackerClient(group)
    assert client.tracker_group is group
    client2 = TrackerClient()
    assert client2.tracker_group is not None
    client.errno = 10
    assert client.getErrorCode() == 10

def test_get_tracker_server_public():
    group = DummyTrackerGroup()
    server = DummyTrackerServer()
    group.tracker_servers = [server]
    group.getTrackerServer = lambda: server
    client = TrackerClient(group)
    assert client.getTrackerServer() is server

def test_get_connection_failover_public():
    group = DummyTrackerGroup()
    server1 = DummyTrackerServer()
    server2 = DummyTrackerServer()
    # Simulate server1.getConnection throws
    server1.getConnection = mock.Mock(side_effect=Exception("fail1"))
    group.tracker_servers = [server1, server2]
    client = TrackerClient(group)
    res = client.getConnection(None)
    assert res == server2.connection