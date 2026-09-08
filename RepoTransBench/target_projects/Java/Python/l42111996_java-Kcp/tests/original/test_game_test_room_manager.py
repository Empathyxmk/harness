def test_game_test_room_manager_add_remove():
    class TestRoom:
        id_counter = 0
        def __init__(self): self.ukcps = []; TestRoom.id_counter += 1; self.roomId = TestRoom.id_counter
        def size(self): return len(self.ukcps)
        def getUkcps(self): return self.ukcps
        def getRoomId(self): return self.roomId
    class GameTestRoomManager:
        def __init__(self): self.rooms = {}
        def addClient(self, ukcp):
            for r in self.rooms.values():
                if r.size() < 8:
                    r.getUkcps().append(ukcp)
                    return
            new = TestRoom(); new.getUkcps().append(ukcp); self.rooms[new.getRoomId()] = new
        def remove(self, ukcp):
            for room in list(self.rooms.values()):
                if ukcp in room.getUkcps():
                    room.getUkcps().remove(ukcp)
                    if not room.getUkcps(): del self.rooms[room.getRoomId()]
    mgr = GameTestRoomManager()
    ukcp = object()
    mgr.addClient(ukcp)
    assert any(ukcp in room.getUkcps() for room in mgr.rooms.values())
    mgr.remove(ukcp)
    assert not any(ukcp in room.getUkcps() for room in mgr.rooms.values())