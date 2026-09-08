def test_kcp_game_test_server_room_manager():
    class TpsChannelServerCache:
        def __init__(self): self._packids = []
        def addPackId(self, v): self._packids.append(v)
        def size(self): return len(self._packids)
        def getSendPackIds(self): return list(self._packids)
    class TestRoom:
        def __init__(self): self.ukcps = []
        def size(self): return len(self.ukcps)
    class GameTestRoomManager:
        def __init__(self): self.rooms = {}
        def addClient(self, ukcp):
            if not self.rooms: self.rooms[1] = TestRoom()
            self.rooms[1].ukcps.append(ukcp)
        def remove(self, ukcp):
            for room in list(self.rooms.values()):
                try: room.ukcps.remove(ukcp)
                except ValueError: pass
    mgr = GameTestRoomManager()
    ukcp = object()
    mgr.addClient(ukcp)
    assert mgr.rooms[1].size() == 1
    mgr.remove(ukcp)
    assert mgr.rooms[1].size() == 0